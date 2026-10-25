from dataclasses import dataclass

@dataclass
class TemporalState:
    movement: str
    horizontal_speed: float
    vertical_speed: float
    ankle_speed: float


class MovementTracker:
    """Lightweight temporal classifier over normalised pose coordinates."""
    def __init__(self, fps: float = 30.0):
        self.fps = max(float(fps), 1.0)
        self.previous = None

    def update(self, metrics: dict) -> TemporalState:
        hip = metrics['hip_center']
        left_ankle = metrics['left_ankle']
        right_ankle = metrics['right_ankle']
        horizontal = vertical = ankle_speed = 0.0
        if self.previous is not None:
            horizontal = abs(hip[0] - self.previous['hip'][0]) * self.fps
            vertical = (self.previous['hip'][1] - hip[1]) * self.fps
            ankle_speed = max(
                abs(left_ankle[0]-self.previous['left_ankle'][0]),
                abs(right_ankle[0]-self.previous['right_ankle'][0]),
            ) * self.fps
        knees = (metrics['left_knee_angle'] + metrics['right_knee_angle']) / 2
        if vertical > 0.30:
            movement = 'JUMPING'
        elif min(metrics['left_knee_angle'], metrics['right_knee_angle']) < 105 and ankle_speed > 0.20:
            movement = 'KICKING'
        elif horizontal > 0.65:
            movement = 'SPRINTING'
        elif horizontal > 0.22:
            movement = 'RUNNING'
        elif knees < 125 and metrics['torso_lean'] < 30:
            movement = 'DEFENDING'
        else:
            movement = 'CONTROLLED'
        self.previous = {'hip':hip,'left_ankle':left_ankle,'right_ankle':right_ankle}
        return TemporalState(movement, round(horizontal,3), round(vertical,3), round(ankle_speed,3))
