PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS analysis_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_name TEXT NOT NULL,
  player_ref TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'OPEN' CHECK(status IN ('OPEN','COMPLETED')),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS frames (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  frame_number INTEGER NOT NULL CHECK(frame_number >= 0),
  timestamp_ms INTEGER CHECK(timestamp_ms >= 0),
  FOREIGN KEY(session_id) REFERENCES analysis_sessions(id) ON DELETE CASCADE,
  UNIQUE(session_id, frame_number)
);

CREATE TABLE IF NOT EXISTS pose_metrics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  frame_id INTEGER NOT NULL UNIQUE,
  left_knee_angle REAL,
  right_knee_angle REAL,
  hip_angle REAL,
  torso_lean REAL,
  confidence REAL CHECK(confidence IS NULL OR confidence BETWEEN 0 AND 1),
  FOREIGN KEY(frame_id) REFERENCES frames(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS posture_predictions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  frame_id INTEGER NOT NULL,
  label TEXT NOT NULL,
  confidence REAL NOT NULL CHECK(confidence BETWEEN 0 AND 1),
  model_version TEXT NOT NULL DEFAULT 'geometry-baseline-v1',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(frame_id) REFERENCES frames(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_frames_session ON frames(session_id);
CREATE INDEX IF NOT EXISTS idx_predictions_frame ON posture_predictions(frame_id);
