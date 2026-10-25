import json
import os
import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from src.pipeline import analyse_keypoint_sequence
from src.product_storage import persist_sequence, session_history
from src.reporting import summarise_analysis, to_markdown
from src.video_pipeline import analyse_video

ROOT = Path(__file__).resolve().parent
UPLOADS = ROOT / 'uploads'
ARTIFACTS = ROOT / 'artifacts'
UPLOADS.mkdir(exist_ok=True)
ARTIFACTS.mkdir(exist_ok=True)

app = Flask(__name__)
app.config.update(MAX_CONTENT_LENGTH=80*1024*1024, DATABASE=os.getenv('FOOTBALL_DB', str(ROOT/'football.db')))


@app.get('/')
def index():
    return render_template('index.html')


def finish_result(source_name, player_ref, results, artifact_name=None):
    session_id = persist_sequence(app.config['DATABASE'], source_name, player_ref, results)
    summary = summarise_analysis(results)
    report_name = f'report-{session_id}.md'
    (ARTIFACTS/report_name).write_text(to_markdown(summary, source_name), encoding='utf-8')
    return {
        'session_id':session_id,
        'summary':summary,
        'samples':results[:80],
        'annotated_video_url':f'/artifacts/{artifact_name}' if artifact_name else None,
        'report_url':f'/artifacts/{report_name}',
        'history':session_history(app.config['DATABASE']),
    }


@app.post('/api/analyse-keypoints')
def analyse_keypoints():
    payload = request.get_json(silent=True) or {}
    frames = payload.get('frames') or []
    if not frames:
        return jsonify({'error':'frames are required'}), 400
    if len(frames) > 5000:
        return jsonify({'error':'too many frames'}), 400
    try:
        results = analyse_keypoint_sequence(frames, float(payload.get('fps',30)))
    except (ValueError, TypeError) as exc:
        return jsonify({'error':str(exc)}), 400
    return jsonify(finish_result(payload.get('source_name','keypoint-sequence'), payload.get('player_ref','player-1'), results))


@app.post('/api/analyse-video')
def analyse_video_route():
    file = request.files.get('video')
    if not file or not file.filename:
        return jsonify({'error':'video file is required'}), 400
    ext = Path(file.filename).suffix.lower()
    if ext not in {'.mp4','.mov','.avi','.mkv'}:
        return jsonify({'error':'supported formats: MP4, MOV, AVI, MKV'}), 400
    token = uuid.uuid4().hex[:10]
    safe = secure_filename(file.filename)
    input_path = UPLOADS / f'{token}-{safe}'
    artifact_name = f'annotated-{token}.mp4'
    output_path = ARTIFACTS / artifact_name
    file.save(input_path)
    try:
        result = analyse_video(input_path, output_path=output_path, sample_every=2)
    except RuntimeError as exc:
        return jsonify({'error':str(exc),'hint':'Install requirements-cv.txt for MediaPipe/OpenCV video support.'}), 503
    except Exception as exc:
        return jsonify({'error':f'video analysis failed: {exc}'}), 400
    finally:
        input_path.unlink(missing_ok=True)
    return jsonify(finish_result(safe, request.form.get('player_ref','player-1'), result['samples'], artifact_name=artifact_name))


@app.get('/api/history')
def history():
    return jsonify(session_history(app.config['DATABASE']))


@app.get('/artifacts/<path:name>')
def artifact(name):
    return send_from_directory(ARTIFACTS, name, as_attachment=name.endswith('.md'))


@app.get('/health')
def health():
    return jsonify({'status':'ok','service':'football-posture-analysis'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT','5000')), debug=True)
