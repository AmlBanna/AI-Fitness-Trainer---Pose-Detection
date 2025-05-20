# 💪 AI Pose Exercise Counter

![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8%2B-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)

Real-time bicep curl counter using MediaPipe pose detection with angle calculation.


## ✨ Features
- Real-time pose tracking
- Accurate angle calculation
- Repetition counter
- Form feedback
- FPS performance display

## 🚀 Quick Start

### Installation
```bash
pip install mediapipe opencv-python numpy
```
### Usage
```bash
python exercise_counter.py
```
## 🛠 Technical Implementation
### Key Components
```python
# Pose Detection Initialization
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Angle Calculation
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180/np.pi)
    return 360 - angle if angle > 180 else angle
```
## 📊 Exercise Counter Logic

| Stage       | Angle Range | Action                  | Visual Indicator      |
|-------------|-------------|-------------------------|-----------------------|
| **Down**    | >160°       | Prepares for next rep   | 🔵 Blue Stage Text    |
| **Up**      | <45°        | Counts completed rep    | 🟢 Counter Increment  |

### 💡 How the Counter Works:
```python
if angle > 160:    # Down position threshold
    stage = "Down"
if angle < 45 and stage == "Down":  # Up position threshold
    stage = "Up"
    counter += 1  # Increment rep count
```
### 🎚️ Threshold Customization:
```python
# Adjust these values in the code:
DOWN_THRESHOLD = 160  # Default: 160° (more strict if decreased)
UP_THRESHOLD = 45     # Default: 45°  (more strict if increased)
```
### 🔍 Form Tips:
1.Keep elbow stationary during curls

2.Maintain 90° angle at bottom position

3.Full extension at top triggers count

### 💡 Customization
### Adjustable Parameters
```python
# Confidence thresholds
pose = mp_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Angle thresholds
DOWN_ANGLE = 160  # Default: 160°
UP_ANGLE = 40     # Default: 45°
```
