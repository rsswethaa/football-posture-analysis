from .biomechanics import extract_biomechanics
from .temporal import MovementTracker


def analyse_keypoint_sequence(frames: list[dict], fps: float = 30.0) -> list[dict]:
    tracker = MovementTracker(fps=fps)
    results = []
    for index, frame in enumerate(frames):
        points = frame.get('points', frame)
        confidence = frame.get('confidence', 1.0) if isinstance(frame, dict) else 1.0
        metrics = extract_biomechanics(points, confidence=confidence)
        state = tracker.update(metrics)
        results.append({
            'frame_number': frame.get('frame_number', index) if isinstance(frame, dict) else index,
            'timestamp_ms': frame.get('timestamp_ms', round(index / max(fps,1) * 1000)) if isinstance(frame, dict) else round(index / max(fps,1) * 1000),
            'movement': state.movement,
            'horizontal_speed': state.horizontal_speed,
            'vertical_speed': state.vertical_speed,
            'ankle_speed': state.ankle_speed,
            'metrics': metrics,
        })
    return results
