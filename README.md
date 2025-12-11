
# Monkey Pose Mimic

> Real-time pose detection desktop app with animated monkey character using MediaPipe and OpenCV

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://claude.ai/chat/LICENSE)

---

## 📖 About

Monkey Pose Mimic detects your movements through your webcam and displays them using an animated monkey character. The app uses MediaPipe for pose detection and OpenCV for real-time video processing.

### Supported Poses

* **🙋 Raising Hand** - Both hands raised above head
* **😲 Shocking** - Mouth wide open
* **🤔 Thinking** - Hand near face or chin
* **🙂 Normal** - Default neutral pose

---

## ✨ Features

* **Real-time pose detection** using MediaPipe
* **4 different poses** automatically detected
* **Multi-language support** (English, Indonesian, Turkish)
* **Modern UI** with macOS-inspired design
* **Customizable settings** through config file
* **Landmark visibility toggle** - Show/hide detection lines

---

## 🛠️ Requirements

### Software

* **Python 3.12.x** (Required - MediaPipe doesn't support Python 3.13+)
* **Webcam** (built-in or external)
* **OS:** Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)

### Hardware

* **Minimum:** Intel Core i3, 4GB RAM, 640x480 webcam
* **Recommended:** Intel Core i5+, 8GB RAM, 720p+ webcam

---

## 🚀 Quick Start

### 1. Install Python

**Important:** MediaPipe requires Python 3.12 or lower.

Download Python 3.12.8:

* **Windows:** [Download](https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe)
* **macOS:** [Download](https://www.python.org/ftp/python/3.12.8/python-3.12.8-macos11.pkg)
* **Linux:** Use your package manager

```bash
# Ubuntu/Debian
sudo apt install python3.12 python3.12-venv
```

### 2. Clone & Setup

```bash
# Clone repository
git clone https://github.com/beyzatanriverdi/monkey_pose_mimic.git
cd monkey_pose_mimic

# Run setup script
# Windows:
setup.bat

# macOS/Linux:
chmod +x setup.sh
./setup.sh
```

### 3. Run Application

```bash
# Windows:
run.bat

# macOS/Linux:
./run.sh
```

---

## 📚 How to Use

1. **Launch** the application
2. **Allow** camera access when prompted
3. **Position yourself** 1-2 meters from the camera
4. **Try different poses:**
   * Raise both hands above your head
   * Open your mouth wide
   * Put your hand near your face
   * Stand normally

The monkey character will mirror your pose in real-time!

---

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
# Camera settings
class CameraConfig:
    device_id: int = 0      # Camera ID (try 0, 1, 2...)
    width: int = 640        # Resolution
    height: int = 480
    fps: int = 40           # Frame rate

# Detection sensitivity
class PoseDetectionConfig:
    hand_raise_threshold: float = 0.05
    mouth_open_threshold: float = 0.15
    hand_to_face_threshold: float = 0.08
```

---

## 🐛 Troubleshooting

### Camera Not Detected

Try changing camera ID in `config.py`:

```python
device_id: int = 1  # Try 0, 1, 2, etc.
```

### MediaPipe Error

Check Python version:

```bash
python --version  # Should show Python 3.12.x
```

### Slow Performance

Reduce resolution in `config.py`:

```python
width: int = 320
height: int = 240
fps: int = 20
```

### Need More Help?

* Check [Issues](https://github.com/beyzatanriverdi/monkey_pose_mimic/issues)
* Create a new issue with:
  * Python version
  * Operating system
  * Complete error message

---

## 📦 Project Structure

```
monkey_pose_mimic/
├── main.py              # Application entry point
├── pose_detector.py     # Pose detection logic
├── config.py            # Settings
├── requirements.txt     # Dependencies
├── assets/              # Monkey images
│   ├── default_pose.jpg
│   ├── raising_hand_pose.jpg
│   ├── shocking_pose.jpg
│   └── thinking_pose.jpg
└── README.md           # This file
```

---

## 🛠️ Tech Stack

| Library   | Version | Purpose                  |
| --------- | ------- | ------------------------ |
| Python    | 3.12.x  | Programming language     |
| MediaPipe | 0.10.14 | Pose/hand/face detection |
| OpenCV    | 4.10.0  | Video processing         |
| PyQt5     | 5.15.11 | User interface           |
| NumPy     | 1.26.4  | Numerical operations     |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate documentation.

---

## 👥 Authors

### Beyza Tanriverdi

* 📧 Email: tnrvrd.beyza@gmail.com
* 🐙 GitHub: [@beyzatanriverdi](https://github.com/beyzatanriverdi)
* 💼 LinkedIn: [Beyza Tanriverdi](https://www.linkedin.com/in/beyza-tanr1verdi-8a46b0364)

### Kadir Talha Uncu

* 📧 Email: talhauncu.dev@gmail.com
* 🐙 GitHub: [@talhauncu](https://github.com/talhauncu)
* 💼 LinkedIn: [Kadir Talha Uncu](https://www.linkedin.com/in/kadir-talha-uncu-622186339)

---

## 📄 License

This project is licensed under the [MIT License](https://claude.ai/chat/LICENSE) - feel free to use, modify, and distribute as you wish.

---

## 🙏 Acknowledgments

Built with these amazing technologies:

* [Google MediaPipe](https://mediapipe.dev/) - ML framework
* [OpenCV](https://opencv.org/) - Computer vision library
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework

---

## 📖 Citation

If you use this project in your research, please cite:

```bibtex
@software{monkey_pose_mimic,
  author = {Tanriverdi, Beyza and Uncu, Kadir Talha},
  title = {Monkey Pose Mimic: Real-time Pose Detection},
  year = {2024},
  url = {https://github.com/beyzatanriverdi/monkey_pose_mimic}
}
```

---

<div align="center">
**Made with ❤️ by Beyza Tanriverdi & Kadir Talha Uncu**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/beyzatanriverdi/monkey_pose_mimic/issues) · [Request Feature](https://github.com/beyzatanriverdi/monkey_pose_mimic/issues)

</div>
