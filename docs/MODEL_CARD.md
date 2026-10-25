# Model Card — Geometry Baseline v1

## Purpose
Educational posture-analysis baseline operating on body keypoints.

## Inputs
2D keypoints or derived joint-angle features.

## Outputs
Interpretable posture label and confidence-like score.

## Limitations
No real-camera benchmark accuracy is established. 2D geometry is sensitive to viewpoint, occlusion, tracking errors and pose-estimator quality. Confidence is not a calibrated probability.

## DL extension
A research version could use MoveNet/OpenPose-style keypoints plus temporal CNN/LSTM/Transformer models with documented training data and evaluation.
