# Monkey Pose Mimic

> Aplikasi desktop interaktif untuk deteksi pose real-time dengan karakter monyet berbasis MediaPipe dan OpenCV

[English](https://claude.ai/chat/README.md) | **Bahasa Indonesia** | [Türkçe](https://claude.ai/chat/README.tr.md)

---

## Deskripsi

Monkey Pose Mimic adalah aplikasi desktop yang mendeteksi gerakan user melalui camera dan menampilkan representasi visual menggunakan character monyet animasi. Aplikasi ini memanfaatkan teknologi MediaPipe untuk pose detection dan OpenCV untuk video processing real-time.

### Pose yang Didukung

* **Raising Hand** - Kedua tangan diangkat di atas kepala
* **Shocking Expression** - Mulut terbuka lebar
* **Thinking Pose** - Tangan di dekat wajah atau dagu
* **Normal Position** - Pose netral default

---

## Features

### Version 2.0.0

* **Modern Python Architecture** - Menggunakan type hints Python 3.12, dataclass, dan best practices
* **Comprehensive Logging** - System logging untuk debugging dan monitoring
* **Centralized Configuration** - Management konfigurasi terpusat melalui `config.py`
* **Enhanced Error Handling** - Error handling yang robust dan informatif
* **Modern Packaging** - Menggunakan `pyproject.toml` untuk packaging
* **Multi-language Support** - Dokumentasi dalam bahasa Indonesia, Inggris, dan Turki

---

## System Requirements

### Software

* **Python 3.12.x** (Wajib - MediaPipe tidak kompatibel dengan Python 3.13+)
* **Webcam** (Built-in atau eksternal)
* **Operating System:** Windows 10/11, macOS 10.15+, atau Linux (Ubuntu 20.04+)

### Hardware (Minimum)

* **Processor:** Intel Core i3 atau setara
* **RAM:** 4 GB
* **Webcam:** Resolusi minimum 640x480

### Hardware (Recommended)

* **Processor:** Intel Core i5 atau lebih tinggi
* **RAM:** 8 GB atau lebih
* **Webcam:** Resolusi 720p atau lebih tinggi

---

## Installation

### Step 1: Install Python 3.12

**PENTING:** MediaPipe saat ini tidak mendukung Python 3.13 atau versi lebih tinggi.

#### Download Python 3.12.8

* **Windows:** [python-3.12.8-amd64.exe](https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe)
* **macOS:** [python-3.12.8-macos11.pkg](https://www.python.org/ftp/python/3.12.8/python-3.12.8-macos11.pkg)
* **Linux:** Gunakan package manager distribusi Anda

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3.12-venv

# Fedora
sudo dnf install python3.12

# Arch Linux
sudo pacman -S python312
```

### Step 2: Clone Repository

```bash
git clone https://github.com/beyzatanriverdi/monkey_pose_mimic.git
cd monkey_pose_mimic
```

### Step 3: Setup Environment

#### Automatic Method (Recommended)

**Windows:**

```bash
setup.bat
```

**macOS/Linux:**

```bash
chmod +x setup.sh
./setup.sh
```

#### Manual Method

```bash
# Buat virtual environment
python3.12 -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

## How to Run

### Quick Method

**Windows:**

```bash
run.bat
```

**macOS/Linux:**

```bash
chmod +x run.sh
./run.sh
```

### Manual Method

**Dengan virtual environment:**

```bash
# Aktifkan virtual environment terlebih dahulu
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

python main.py
```

**Tanpa virtual environment:**

```bash
# Windows
py -3.12 main.py

# macOS/Linux
python3.12 main.py
```

---

## Usage Guide

1. **Run aplikasi** menggunakan salah satu method di atas
2. **Allow camera access** ketika browser atau system meminta permission
3. **Position diri** di tengah frame camera dengan jarak 1-2 meter
4. **Lakukan berbagai pose:**
   * Angkat kedua tangan di atas kepala untuk pose "Raising Hand"
   * Buka mulut lebar-lebar untuk pose "Shocking"
   * Letakkan tangan di dekat wajah atau dagu untuk pose "Thinking"
   * Berdiri netral untuk pose "Default"

Character monyet akan secara otomatis mimic pose Anda dalam real-time.

---

## Technology Stack

### Core Dependencies

| Library   | Version | Function                       |
| --------- | ------- | ------------------------------ |
| Python    | 3.12.x  | Programming language utama     |
| MediaPipe | 0.10.14 | Pose, hand, dan face detection |
| OpenCV    | 4.10.0  | Video dan image processing     |
| PyQt5     | 5.15.11 | GUI framework                  |
| NumPy     | 1.26.4  | Numeric computation            |

### Development Tools (Optional)

* **Black** - Code formatter untuk Python
* **Mypy** - Static type checker
* **Ruff** - Fast linter
* **Pytest** - Testing framework

---

## Project Structure

```
monkey_pose_mimic/
├── main.py                  # Application entry point
├── pose_detector.py         # MediaPipe pose detection module
├── config.py               # Centralized configuration file
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Modern project configuration
├── LICENSE                # MIT License
├── setup.bat              # Setup script untuk Windows
├── setup.sh               # Setup script untuk macOS/Linux
├── run.bat                # Run script untuk Windows
├── run.sh                 # Run script untuk macOS/Linux
├── assets/                # Image assets
│   ├── default_pose.jpg
│   ├── raising_hand_pose.jpg
│   ├── shocking_pose.jpg
│   └── thinking_pose.jpg
├── README.md              # Documentation (English)
├── README.id.md           # Documentation (Bahasa Indonesia)
└── README.tr.md           # Documentation (Türkçe)
```

---

## Configuration

Anda dapat customize behavior aplikasi melalui file `config.py`:

### Camera Configuration

```python
class CameraConfig:
    device_id: int = 0        # Camera device ID (0, 1, 2, ...)
    width: int = 640          # Resolution width
    height: int = 480         # Resolution height
    fps: int = 40             # Frames per second
```

### Pose Detection Configuration

```python
class PoseDetectionConfig:
    hand_raise_threshold: float = 0.05   # Hand raise detection sensitivity
    mouth_open_threshold: float = 0.15   # Mouth open detection sensitivity
    hand_face_distance_threshold: float = 0.15  # Hand to face distance
```

### Logging Configuration

```python
class LoggingConfig:
    level: str = "INFO"                  # DEBUG, INFO, WARNING, ERROR
    format: str = "%(asctime)s - %(levelname)s - %(message)s"
    log_to_file: bool = False           # Save log ke file
    log_file: str = "monkey_pose.log"
```

---

## Troubleshooting

### Common Issues

#### Camera tidak terdeteksi

**Solution:**

```python
# Edit config.py, ubah device_id
class CameraConfig:
    device_id: int = 1  # Coba nilai 0, 1, 2, dst.
```

Atau check available camera devices:

```bash
python -c "import cv2; [print(f'Camera {i}') for i in range(5) if cv2.VideoCapture(i).isOpened()]"
```

#### MediaPipe Error

**Root cause:** Python version tidak sesuai

**Solution:**

```bash
python --version  # Pastikan output: Python 3.12.x
```

Jika menggunakan Python 3.13+, uninstall dan install Python 3.12.

#### Slow Performance

**Solution:**

1. Close aplikasi lain yang menggunakan camera
2. Reduce resolution di `config.py`:

```python
class CameraConfig:
    width: int = 320
    height: int = 240
    fps: int = 20
```

3. Pastikan tidak ada background process yang heavy

#### Dependencies Error

**Solution:**

```bash
# Hapus virtual environment lama
rm -rf venv  # Linux/macOS
# atau
rmdir /s venv  # Windows

# Buat virtual environment baru
python3.12 -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate di Windows

# Install ulang dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Getting Help

Jika issue masih berlanjut:

1. Check [Issues](https://github.com/beyzatanriverdi/monkey_pose_mimic/issues) yang sudah ada
2. Create issue baru dengan informasi:
   * Python version (`python --version`)
   * Operating system
   * Error message lengkap
   * Steps untuk reproduce issue

---

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Atau install secara individual
pip install black mypy ruff pytest
```

### Code Quality Tools

```bash
# Format code
black .

# Type checking
mypy main.py pose_detector.py

# Linting
ruff check .

# Run tests
pytest
```

### Contribution Guidelines

1. Fork repository ini
2. Create branch untuk feature baru (`git checkout -b feature/NamaFitur`)
3. Pastikan code mengikuti style guide:
   * Gunakan Black untuk formatting
   * Add type hints
   * Write docstrings untuk public functions
4. Commit changes (`git commit -m 'Menambahkan fitur X'`)
5. Push ke branch (`git push origin feature/NamaFitur`)
6. Create Pull Request dengan description yang jelas

---

## Roadmap

### Planned Features

* [ ] Support untuk lebih banyak pose
* [ ] Multiple character options

---

## Development Team

### Beyza Tanriverdi

* **Email:** tnrvrd.beyza@gmail.com
* **GitHub:** [@beyzatanriverdi](https://github.com/beyzatanriverdi)
* **LinkedIn:** [Beyza Tanriverdi](https://www.linkedin.com/in/beyza-tanr1verdi-8a46b0364)

### Kadir Talha Uncu

* **Email:** talhauncu.dev@gmail.com
* **GitHub:** [@talhauncu](https://github.com/talhauncu)
* **LinkedIn:** [Kadir Talha Uncu](https://www.linkedin.com/in/kadir-talha-uncu-622186339)

---

## License

Project ini dilisensikan di bawah [MIT License](https://claude.ai/chat/LICENSE). Anda bebas untuk use, modify, dan distribute software ini sesuai dengan terms of license.

---

## Acknowledgments

Project ini tidak akan terwujud tanpa support dari:

* **[Google MediaPipe](https://mediapipe.dev/)** - Powerful machine learning framework
* **[OpenCV](https://opencv.org/)** - Open-source computer vision library
* **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/)** - Cross-platform GUI framework

---

## Citation

Jika Anda menggunakan project ini dalam research atau publication, mohon cantumkan reference berikut:

```bibtex
@software{monkey_pose_mimic,
  author = {Tanriverdi, Beyza and Uncu, Kadir Talha},
  title = {Monkey Pose Mimic: Real-time Pose Detection with Interactive Character},
  year = {2024},
  url = {https://github.com/beyzatanriverdi/monkey_pose_mimic}
}
```

---

<div align="center">
**Developed dengan ❤️ oleh Beyza Tanriverdi & Kadir Talha Uncu**

⭐ Jika project ini bermanfaat, berikan star di GitHub!

[Report Bug](https://github.com/beyzatanriverdi/monkey_pose_mimic/issues) · [Request Feature](https://github.com/beyzatanriverdi/monkey_pose_mimic/issues) · [Documentation](https://github.com/beyzatanriverdi/monkey_pose_mimic/wiki)

</div>
