# Football Posture Analysis

A deep-learning-inspired computer-vision portfolio project for analysing football player posture from body keypoints and classifying movement patterns.

## Features
- 2D pose/keypoint representation
- joint-angle calculation
- posture feature extraction
- interpretable posture classification baseline
- synthetic keypoint samples
- tests, CI, architecture and technical report

## Architecture
```mermaid
flowchart LR
  V[Video frame] --> P[Pose estimator]
  P --> K[Body keypoints]
  K --> F[Angles + posture features]
  F --> C[Posture classifier]
  C --> R[Player posture report]
```

## Run
```bash
python demo.py
python -m unittest discover -s tests -v
```

A production DL version would connect the feature layer to a trained pose-estimation and temporal classification model. This repository does not claim benchmark accuracy without a documented dataset and evaluation run.
