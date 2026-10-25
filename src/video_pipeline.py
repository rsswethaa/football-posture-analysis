from pathlib import Path

from .biomechanics import extract_biomechanics
from .temporal import MovementTracker


def _load_cv():
    try:
        import cv2
        import mediapipe as mp
    except ImportError as exc:
        raise RuntimeError('Install requirements-cv.txt to enable video analysis') from exc
    return cv2, mp


def analyse_video(input_path, output_path=None, sample_every=2, max_frames=1800):
    """Analyse the primary visible player with MediaPipe Pose and optionally write an annotated video."""
    cv2, mp = _load_cv()
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise ValueError('Unable to open video file')
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
    writer = None
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        writer = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    pose_module = mp.solutions.pose
    drawing = mp.solutions.drawing_utils
    tracker = MovementTracker(fps=fps / max(sample_every, 1))
    results = []
    frame_number = 0
    with pose_module.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=.5, min_tracking_confidence=.5) as pose:
        while frame_number < max_frames:
            ok, frame = cap.read()
            if not ok:
                break
            movement_label = None
            if frame_number % max(sample_every,1) == 0:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detected = pose.process(rgb)
                if detected.pose_landmarks:
                    lm = detected.pose_landmarks.landmark
                    P = pose_module.PoseLandmark
                    def point(name):
                        item = lm[getattr(P, name).value]
                        return (float(item.x), float(item.y))
                    points = {
                        'left_shoulder':point('LEFT_SHOULDER'),'right_shoulder':point('RIGHT_SHOULDER'),
                        'left_hip':point('LEFT_HIP'),'right_hip':point('RIGHT_HIP'),
                        'left_knee':point('LEFT_KNEE'),'right_knee':point('RIGHT_KNEE'),
                        'left_ankle':point('LEFT_ANKLE'),'right_ankle':point('RIGHT_ANKLE'),
                    }
                    confidence = sum(lm[getattr(P,n).value].visibility for n in ['LEFT_SHOULDER','RIGHT_SHOULDER','LEFT_HIP','RIGHT_HIP','LEFT_KNEE','RIGHT_KNEE','LEFT_ANKLE','RIGHT_ANKLE']) / 8
                    metrics = extract_biomechanics(points, confidence)
                    state = tracker.update(metrics)
                    movement_label = state.movement
                    results.append({'frame_number':frame_number,'timestamp_ms':round(frame_number/fps*1000),'movement':state.movement,'horizontal_speed':state.horizontal_speed,'vertical_speed':state.vertical_speed,'ankle_speed':state.ankle_speed,'metrics':metrics})
                    if writer:
                        drawing.draw_landmarks(frame, detected.pose_landmarks, pose_module.POSE_CONNECTIONS)
            if writer:
                if movement_label:
                    cv2.putText(frame, movement_label, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                writer.write(frame)
            frame_number += 1
    cap.release()
    if writer:
        writer.release()
    return {'fps':fps,'frames_total':frame_number,'samples':results,'annotated_video':str(output_path) if output_path else None}
