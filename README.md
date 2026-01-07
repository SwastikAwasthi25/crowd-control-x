# Crowd Control X – Real-Time Crowd Detection System

## Overview
Crowd Control X is a real-time computer vision system designed to monitor crowd density in public spaces and generate alerts when occupancy exceeds safe limits.

## Problem Statement
Large public gatherings such as religious events, festivals, and rallies face serious safety risks due to overcrowding and delayed response.

## Solution
The system uses a YOLOv8-based detection pipeline to count people from live camera feeds. When the crowd size exceeds a predefined threshold, the system triggers voice alerts and sends SMS notifications to concerned authorities.

## Technology Stack
- Python
- YOLOv8 (Ultralytics)
- OpenCV
- Twilio API
- Text-to-Speech (pyttsx3)

## Key Features
- Real-time people detection and counting  
- Threshold-based alert mechanism  
- Voice alerts for immediate on-site awareness  
- SMS alerts for remote authority notification  
- Cooldown mechanism to prevent alert flooding  

## System Flow
1. Capture live video feed  
2. Detect people using YOLOv8  
3. Count detected individuals  
4. Trigger alerts when threshold is exceeded  

## Use Cases
- Religious gatherings (Kumbh Mela, Hajj)  
- Public events and rallies  
- Crowded transit areas  

## Learnings
- Real-time computer vision deployment  
- Model inference optimization  
- Alert system design  
- Secure API credential handling  
