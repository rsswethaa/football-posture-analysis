# Architecture

```mermaid
sequenceDiagram
  participant F as Video Frame
  participant P as Pose Estimator
  participant G as Geometry Layer
  participant C as Classifier
  F->>P: player image
  P-->>G: shoulder/hip/knee/ankle keypoints
  G->>G: joint angles + posture features
  G-->>C: feature vector
  C-->>F: posture label
```

The repository implements the geometry and classification layers directly. A full DL pipeline would use a trained pose-estimation network for keypoint extraction and optionally a temporal network over frame sequences.
