# Python Tetris Game with Hand Gesture Controls 👋

🕹️ A Tetris game built with Python, pygame, OpenCV, and MediaPipe that lets you play using **hand gestures**! 🤖✋ Control blocks with simple hand movements captured through your webcam - no keyboard required!

## 🎮 Game Controls

### Keyboard Controls (Traditional)
- **↑ Arrow Key**: Rotate block
- **↓ Arrow Key**: Move block down faster
- **← Arrow Key**: Move block left
- **→ Arrow Key**: Move block right

### 👋 Hand Gesture Controls (New!)
- **Move Hand Left**: Move block left (open hand, move significantly left)
- **Move Hand Right**: Move block right (open hand, move significantly right)
- **Close Fist**: Rotate block (all fingers close to palm)
- **Point Up**: Alternative rotate gesture
- **Point Down**: Fast drop (make blocks fall quickly)

If you want to learn how to build your own Tetris game with pygame, check out the accompanying <a href="https://youtu.be/nF_crEtmpBo">Video Tutorial on YouTube.</a> 🎬👨‍💻 This project extends that tutorial by adding computer vision capabilities for gesture-based control. ☕

## 📋 Prerequisites

To run this gesture-controlled Tetris game, you'll need:

```bash
pip install pygame opencv-python mediapipe numpy
```

### Required Libraries:
- **pygame**: Game development framework
- **opencv-python**: Computer vision operations
- **mediapipe**: Hand landmark detection
- **numpy**: Mathematical operations

## 🚀 How to Run

1. **Clone the repository**
2. **Install dependencies**: `pip install pygame opencv-python mediapipe numpy`
3. **Connect a webcam** to your computer
4. **Run the game**: `python main.py`
5. **Position your hand** in front of the camera
6. **Start playing** with gestures or keyboard!
