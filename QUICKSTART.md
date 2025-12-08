# =€ Quick Start Guide

Get Monkey Pose Mimic up and running in 2 minutes!

---

## Prerequisites

1. **Python 3.12.x** installed
   - Download: https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe
   -   Python 3.13+ won't work (MediaPipe limitation)

2. **Webcam** connected to your computer

---

## Installation (Choose One Method)

### Method 1: Automated Setup (Recommended) P

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Method 2: Manual Setup

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the App

### Method 1: Using Run Scripts (Recommended) P

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
./run.sh
```

### Method 2: Manual Run

```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run the app
python main.py
```

---

## Using the App

1. **Allow camera access** when prompted
2. **Position yourself** in front of the webcam
3. **Try these poses:**
   - =K **Raise your hand** above your head
   - =2 **Open your mouth wide** (shocked expression)
   - > **Put your hand near your face/chin** (thinking pose)
   - =B **Stand normally** for default pose

The monkey character will mimic your poses in real-time!

---

## Troubleshooting

### "Python 3.12 not found"
Install Python 3.12 from the link above and make sure it's in your PATH.

### "Camera not working"
- Check if another app is using the camera
- Try changing `device_id` in `config.py`:
  ```python
  class CameraConfig:
      device_id: int = 1  # Try 0, 1, 2, etc.
  ```

### "MediaPipe import error"
Make sure you're using Python 3.12, not 3.13+:
```bash
python --version  # Should show 3.12.x
```

### Low FPS / Lag
Edit `config.py`:
```python
class CameraConfig:
    width: int = 320   # Lower resolution
    height: int = 240
    fps: int = 30      # Lower FPS
```

---

## Next Steps

- Read [README.md](README.md) for full documentation
- Read [README.id.md](README.id.md) for Indonesian documentation
- Check [CHANGELOG.md](CHANGELOG.md) for version history
- Customize settings in `config.py`

---

## Need Help?

- Check the [README.md](README.md) troubleshooting section
- Open an issue on GitHub
- Contact the developers (see README.md)

---

**Enjoy mimicking with the monkey! =5**
