from .geometry import angle

REQUIRED = {"shoulder","hip","knee","ankle"}

def extract_features(points: dict) -> dict:
    missing = REQUIRED - points.keys()
    if missing:
        raise ValueError(f"missing keypoints: {sorted(missing)}")
    knee_angle = angle(points["hip"], points["knee"], points["ankle"])
    hip_angle = angle(points["shoulder"], points["hip"], points["knee"])
    return {"knee_angle": knee_angle, "hip_angle": hip_angle}

def classify_posture(features: dict) -> str:
    knee = features["knee_angle"]
    hip = features["hip_angle"]
    if knee < 115 and hip < 150:
        return "LOW_STANCE"
    if knee > 155 and hip > 160:
        return "UPRIGHT"
    return "DYNAMIC"
