INSERT INTO analysis_sessions(source_name, player_ref, status)
SELECT 'synthetic_demo.mp4', 'PLAYER-01', 'OPEN'
WHERE NOT EXISTS (SELECT 1 FROM analysis_sessions WHERE source_name='synthetic_demo.mp4' AND player_ref='PLAYER-01');

INSERT INTO frames(session_id, frame_number, timestamp_ms)
SELECT id, 0, 0 FROM analysis_sessions WHERE source_name='synthetic_demo.mp4' AND player_ref='PLAYER-01'
AND NOT EXISTS (SELECT 1 FROM frames f JOIN analysis_sessions s ON s.id=f.session_id WHERE s.source_name='synthetic_demo.mp4' AND f.frame_number=0);
