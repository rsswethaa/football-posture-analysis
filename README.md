# Football Posture Analysis

A complete computer-vision portfolio system for converting player body keypoints into interpretable posture features, classifications, persistent analysis records and reviewable reports.

## Included
- 2D pose/keypoint geometry and joint-angle extraction
- interpretable posture-classification baseline
- synthetic keypoint examples
- SQLite database for sessions, frames, metrics and predictions
- architecture/data-flow/ER diagrams
- automated geometry and storage tests
- CI
- interface, deployment, security and model-card docs
- full technical report

## Architecture
```mermaid
flowchart LR
  V[Video / frame] --> P[Pose estimator]
  P --> K[Body keypoints]
  K --> F[Angles + posture features]
  F --> C[Posture classifier]
  C --> DB[(Analysis database)]
  DB --> R[Player posture report]
```

## Run
```bash
python demo.py
python -m unittest discover -s tests -v
```

## Database
```bash
python -c "from src.storage import init_db; init_db('posture.db', seed=True)"
```

A full deep-learning deployment would add trained pose-estimation and temporal models. This repository intentionally does not claim benchmark accuracy without a documented real dataset and evaluation run.
