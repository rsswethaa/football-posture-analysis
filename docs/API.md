# Interface Contracts

The project currently exposes Python modules rather than a public HTTP API.

Core geometry/classification interfaces live in `src/` and are demonstrated by `demo.py`.

Persistence interfaces:
- `init_db(path, seed=False)`
- `create_session(path, source_name, player_ref)`
- `add_frame_result(path, session_id, frame_number, timestamp_ms, metrics, label, confidence, model_version)`

A video service could wrap these contracts with endpoints for job submission, progress, frame metrics and final reports.
