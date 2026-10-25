import math

def angle(a, b, c):
    """Return ABC joint angle in degrees for 2D points."""
    ba = (a[0]-b[0], a[1]-b[1])
    bc = (c[0]-b[0], c[1]-b[1])
    dot = ba[0]*bc[0] + ba[1]*bc[1]
    norm = math.hypot(*ba) * math.hypot(*bc)
    if norm == 0:
        raise ValueError("joint points must be distinct")
    cos_v = max(-1.0, min(1.0, dot/norm))
    return round(math.degrees(math.acos(cos_v)), 2)
