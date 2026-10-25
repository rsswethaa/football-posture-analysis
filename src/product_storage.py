from pathlib import Path
from .storage import connect, init_db, create_session, add_frame_result


def ensure_ready(db_path):
    path = Path(db_path)
    if not path.exists():
        init_db(path, seed=False)
    return path


def persist_sequence(db_path, source_name, player_ref, results):
    ensure_ready(db_path)
    session_id = create_session(db_path, source_name, player_ref)
    for item in results:
        metrics = item['metrics']
        confidence = max(.25, min(1.0, metrics.get('confidence',1.0)))
        add_frame_result(
            db_path, session_id, item['frame_number'], item.get('timestamp_ms'), metrics,
            item['movement'], confidence, model_version='mediapipe-temporal-rules-v2'
        )
    with connect(db_path) as db:
        db.execute("UPDATE analysis_sessions SET status='COMPLETED' WHERE id=?", (session_id,))
    return session_id


def session_history(db_path, limit=8):
    ensure_ready(db_path)
    with connect(db_path) as db:
        rows = db.execute('''SELECT s.id,s.source_name,s.player_ref,s.status,s.created_at,COUNT(f.id) AS frames
                             FROM analysis_sessions s LEFT JOIN frames f ON f.session_id=s.id
                             GROUP BY s.id ORDER BY s.id DESC LIMIT ?''',(int(limit),)).fetchall()
        return [dict(row) for row in rows]
