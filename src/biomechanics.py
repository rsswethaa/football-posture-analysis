import math
from .geometry import angle

REQUIRED = {
    'left_shoulder','right_shoulder','left_hip','right_hip',
    'left_knee','right_knee','left_ankle','right_ankle'
}


def _mid(a, b):
    return ((a[0]+b[0])/2, (a[1]+b[1])/2)


def _distance(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])


def extract_biomechanics(points: dict, confidence: float = 1.0) -> dict:
    missing = REQUIRED - points.keys()
    if missing:
        raise ValueError(f"missing keypoints: {sorted(missing)}")
    left_knee = angle(points['left_hip'], points['left_knee'], points['left_ankle'])
    right_knee = angle(points['right_hip'], points['right_knee'], points['right_ankle'])
    left_hip_angle = angle(points['left_shoulder'], points['left_hip'], points['left_knee'])
    right_hip_angle = angle(points['right_shoulder'], points['right_hip'], points['right_knee'])
    shoulder_mid = _mid(points['left_shoulder'], points['right_shoulder'])
    hip_mid = _mid(points['left_hip'], points['right_hip'])
    ankle_mid = _mid(points['left_ankle'], points['right_ankle'])
    torso_dx, torso_dy = shoulder_mid[0]-hip_mid[0], shoulder_mid[1]-hip_mid[1]
    torso_lean = abs(math.degrees(math.atan2(torso_dx, -torso_dy)))
    shoulder_width = max(_distance(points['left_shoulder'], points['right_shoulder']), 1e-6)
    stride = _distance(points['left_ankle'], points['right_ankle']) / shoulder_width
    base_width = max(_distance(points['left_ankle'], points['right_ankle']), shoulder_width * .5)
    balance_offset = abs(hip_mid[0] - ankle_mid[0]) / max(base_width, 1e-6)
    balance = max(0.0, min(1.0, 1.0 - balance_offset))
    return {
        'left_knee_angle': round(left_knee, 2),
        'right_knee_angle': round(right_knee, 2),
        'hip_angle': round((left_hip_angle+right_hip_angle)/2, 2),
        'torso_lean': round(torso_lean, 2),
        'stride': round(stride, 3),
        'balance': round(balance, 3),
        'hip_center': hip_mid,
        'left_ankle': points['left_ankle'],
        'right_ankle': points['right_ankle'],
        'confidence': max(0.0, min(1.0, float(confidence))),
    }
