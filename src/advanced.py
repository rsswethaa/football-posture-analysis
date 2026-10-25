import math
from flask import Blueprint, jsonify, request
from .pipeline import analyse_keypoint_sequence

def _centre(points):
    names=['left_shoulder','right_shoulder','left_hip','right_hip']; vals=[points[n] for n in names if n in points]
    if not vals: raise ValueError('player keypoints need shoulder/hip landmarks')
    return (sum(p[0] for p in vals)/len(vals),sum(p[1] for p in vals)/len(vals))

def analyse_multiplayer(frames,fps=30.0,max_match_distance=.22):
    tracks={}; centres={}; next_id=1
    for frame_idx,frame in enumerate(frames):
        detections=frame.get('players') or []; used=set()
        for det in detections:
            points=det.get('points',det); centre=_centre(points); best=None; best_dist=max_match_distance
            for tid,prev in centres.items():
                if tid in used: continue
                d=math.hypot(centre[0]-prev[0],centre[1]-prev[1])
                if d<best_dist: best,best_dist=tid,d
            if best is None: best=f'player-{next_id}'; next_id+=1; tracks[best]=[]
            used.add(best); centres[best]=centre; tracks.setdefault(best,[]).append({'points':points,'confidence':det.get('confidence',1.0),'frame_number':frame.get('frame_number',frame_idx),'timestamp_ms':frame.get('timestamp_ms',round(frame_idx/max(fps,1)*1000))})
    output=[]
    for tid,seq in tracks.items():
        analysed=analyse_keypoint_sequence(seq,float(fps)); counts={}
        for row in analysed: counts[row['movement']]=counts.get(row['movement'],0)+1
        output.append({'player_ref':tid,'samples':len(analysed),'movement_counts':counts,'analysis':analysed})
    return output

def register_advanced(app):
    bp=Blueprint('football_advanced',__name__)
    @bp.post('/api/analyse-multiplayer-keypoints')
    def multiplayer():
        p=request.get_json(silent=True) or {}; frames=p.get('frames') or []
        if not frames: return jsonify({'error':'frames are required'}),400
        if len(frames)>3000: return jsonify({'error':'too many frames'}),400
        try: result=analyse_multiplayer(frames,float(p.get('fps',30)),float(p.get('max_match_distance',.22)))
        except (ValueError,TypeError) as exc: return jsonify({'error':str(exc)}),400
        return jsonify({'players':result,'player_count':len(result)})
    app.register_blueprint(bp)
