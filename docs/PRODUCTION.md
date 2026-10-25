# Production hardening

The sports analytics app now exposes a shared production platform layer backed by `DATABASE_URL` when present, with local SQLite fallback. It includes account registration/login, admin/user RBAC, API keys, rate limits, structured logs, metrics, optional Sentry reporting, model/experiment tracking and CSV audit export.

Multi-player support associates players frame-to-frame using normalized torso-centre proximity and runs the existing temporal biomechanics pipeline independently per track. This is a transparent portfolio tracker, not an identity-recognition system. Real-video multi-player detection can later replace the supplied detection list with a detector/pose model while retaining the same tracking interface.

The lightweight Render deployment runs the dashboard and synthetic/keypoint APIs. The optional CV image remains available for MediaPipe/OpenCV workloads that need more memory/CPU.
