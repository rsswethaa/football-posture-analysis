-- Frame-level posture audit
SELECT s.player_ref, f.frame_number, m.left_knee_angle, m.right_knee_angle,
       m.hip_angle, p.label, p.confidence, p.model_version
FROM frames f
JOIN analysis_sessions s ON s.id=f.session_id
LEFT JOIN pose_metrics m ON m.frame_id=f.id
LEFT JOIN posture_predictions p ON p.frame_id=f.id
ORDER BY s.id, f.frame_number;

-- Label distribution
SELECT label, COUNT(*) AS frame_count, ROUND(AVG(confidence),3) AS avg_confidence
FROM posture_predictions GROUP BY label ORDER BY frame_count DESC;
