from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'database' / 'schema.sql'
SEED = ROOT / 'database' / 'seed.sql'


def connect(db_path):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def init_db(db_path, seed=False):
    with connect(db_path) as db:
        db.executescript(SCHEMA.read_text(encoding='utf-8'))
        if seed:
            db.executescript(SEED.read_text(encoding='utf-8'))
    return Path(db_path)


def create_session(db_path, source_name, player_ref):
    with connect(db_path) as db:
        cur = db.execute('INSERT INTO analysis_sessions(source_name,player_ref) VALUES (?,?)', (source_name, player_ref))
        return cur.lastrowid


def add_frame_result(db_path, session_id, frame_number, timestamp_ms, metrics, label, confidence, model_version='geometry-baseline-v1'):
    with connect(db_path) as db:
        cur = db.execute('INSERT INTO frames(session_id,frame_number,timestamp_ms) VALUES (?,?,?)', (session_id, frame_number, timestamp_ms))
        frame_id = cur.lastrowid
        db.execute('''INSERT INTO pose_metrics(frame_id,left_knee_angle,right_knee_angle,hip_angle,torso_lean,confidence)
                      VALUES (?,?,?,?,?,?)''',
                   (frame_id, metrics.get('left_knee_angle'), metrics.get('right_knee_angle'), metrics.get('hip_angle'), metrics.get('torso_lean'), metrics.get('confidence')))
        db.execute('INSERT INTO posture_predictions(frame_id,label,confidence,model_version) VALUES (?,?,?,?)',
                   (frame_id, label, float(confidence), model_version))
        return frame_id
