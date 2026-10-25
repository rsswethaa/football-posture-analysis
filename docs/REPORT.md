# Technical Report

## Problem
Football analysis often requires translating raw video into interpretable movement and posture information.

## Objective
Create a reproducible pipeline that converts player body keypoints into joint-angle features and posture labels.

## Method
The reference prototype calculates knee and hip angles from 2D coordinates, then applies transparent posture rules. This isolates the downstream analysis layer from the choice of pose-estimation model.

## Deep-learning extension
A full system could use MoveNet, OpenPose or another validated pose network for keypoint detection and a temporal CNN/LSTM/Transformer for movement classification.

## Limitations
No trained weights, match dataset or benchmark metrics are claimed here. Occlusion, camera perspective, multi-player tracking and 3D ambiguity remain important challenges.

## Future work
Video ingestion, player tracking, temporal sequences, 3D pose estimation, annotated football datasets and coach-reviewed evaluation.
