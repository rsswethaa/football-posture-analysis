# Setup and Deployment

## Local
```bash
git clone https://github.com/rsswethaa/football-posture-analysis.git
cd football-posture-analysis
python demo.py
python -m unittest discover -s tests -v
```

Optional DB:
```bash
python -c "from src.storage import init_db; init_db('posture.db', seed=True)"
```

A production-shaped pipeline would use object storage for video, asynchronous workers for pose inference, GPU-capable compute, a managed database, model registry, observability and access-controlled reporting.
