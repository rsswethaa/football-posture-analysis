# Testing Strategy

Automated tests cover joint-angle/feature logic, posture classification behaviour, invalid-input handling and SQLite persistence.

Run:
```bash
python -m unittest discover -s tests -v
```

Future evaluation should include annotated real match footage, player-level train/test separation, occlusion cases, camera-angle variation, confusion matrices, temporal consistency and expert/coach review.
