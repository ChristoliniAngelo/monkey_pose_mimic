# Monkey Pose Mimic

Aplikasi desktop interaktif pendeteksi pose real-time dengan karakter monyet.

[English](README.md) | **Bahasa Indonesia** | [T�rk�e](README.md)

---

## Apa itu Monkey Pose Mimic?

Aplikasi desktop yang mendeteksi pose Anda di depan kamera dan meniru gerakan tersebut dengan karakter monyet di layar menggunakan teknologi MediaPipe dan OpenCV.

**Pose yang Didukung:**

- Mengangkat tangan
- Terkejut (mulut terbuka)
- Berpikir (tangan di wajah)
- Posisi normal

---

## Fitur Terbaru (v2.0.0)

- New Style : Type hints Python 3.12, dataclass, dan best practices
- **Logging**: Sistem logging komprehensif untuk debugging
- **Konfigurasi**: Manajemen konfigurasi terpusat
- **Error Handling**: Penanganan error yang lebih baik
- **pyproject.toml**: Packaging Python modern
- **Dukungan Multibahasa**: README dalam bahasa Indonesia, Inggris, dan Turki

---

## Instalasi

### Persyaratan Sistem

- **Python 3.12.x** (WAJIB - MediaPipe tidak kompatibel dengan Python 3.13+)
- Webcam
- Windows / macOS / Linux

### 1. Install Python 3.12

**PENTING**: MediaPipe tidak bekerja dengan Python 3.13+!

 **Download Python 3.12.8**:

- Windows: [python-3.12.8-amd64.exe](https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe)
- macOS: [python-3.12.8-macos11.pkg](https://www.python.org/ftp/python/3.12.8/python-3.12.8-macos11.pkg)
- Linux: Gunakan package manager Anda

### 2. Clone Repository

```bash
git clone https://github.com/beyzatanriverdi/monkey_pose_mimic
cd monkey_pose_mimic
```

### 3. Setup Virtual Environment (Direkomendasikan)

**Windows:**

```bash
setup.bat
```

**macOS/Linux:**

```bash
chmod +x setup.sh
./setup.sh
```

**Atau secara manual:**

```bash
# Buat virtual environment
python3.12 -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Menjalankan Aplikasi

### Cara Mudah

**Windows:**

```bash
run.bat
```

**macOS/Linux:**

```bash
chmod +x run.sh
./run.sh
```

### Cara Manual

**Dengan virtual environment aktif:**

```bash
python main.py
```

**Tanpa virtual environment (Python 3.12):**

```bash
# Windows:
py -3.12 main.py

# macOS/Linux:
python3.12 main.py
```

---

## Teknologi yang Digunakan

### Inti

- **Python 3.12** - Bahasa pemrograman
- **MediaPipe 0.10.14** - Deteksi pose, tangan, dan wajah
- **OpenCV 4.10.0** - Pemrosesan video dan gambar
- **PyQt5 5.15.11** - Antarmuka pengguna grafis
- **NumPy 1.26.4** - Komputasi numerik

### Development Tools (Opsional)

- **Black** - Code formatter
- **Mypy** - Type checker
- **Ruff** - Linter
- **Pytest** - Testing framework

---

## Struktur Proyek

```
monkey_pose_mimic/
�� main.py                 # Aplikasi utama
�� pose_detector.py        # Modul deteksi pose
�� config.py              # Manajemen konfigurasi
�� requirements.txt       # Dependencies Python
�� pyproject.toml        # Konfigurasi proyek modern
�� setup.bat             # Setup script (Windows)
�� setup.sh              # Setup script (macOS/Linux)
�� run.bat               # Run script (Windows)
�� run.sh                # Run script (macOS/Linux)
�� assets/               # Gambar karakter monyet
   �� default_pose.jpg
   �� raising_hand_pose.jpg
   �� shocking_pose.jpg
   �� thinking_pose.jpg
�� README.md             # Dokumentasi (Turki/Inggris)
�� README.id.md          # Dokumentasi (Indonesia)
```

---

## Cara Menggunakan

1. **Jalankan aplikasi** menggunakan salah satu metode di atas
2. **Izinkan akses kamera** saat diminta
3. **Posisikan diri** di depan kamera
4. **Coba pose berbeda**:
   - Angkat tangan Anda di atas kepala
   - Buka mulut lebar-lebar (ekspresi terkejut)
   - Letakkan tangan di dekat wajah/dagu
   - Posisi normal untuk pose default

Karakter monyet akan meniru pose Anda secara real-time!

---

## Konfigurasi

Anda dapat menyesuaikan aplikasi dengan mengedit `config.py`:

```python
# Contoh: Ubah resolusi kamera
class CameraConfig:
    width: int = 1280  # Default: 640
    height: int = 720  # Default: 480
    fps: int = 60      # Default: 40

# Contoh: Sesuaikan threshold deteksi
class PoseDetectionConfig:
    hand_raise_threshold: float = 0.08  # Default: 0.05
    mouth_open_threshold: float = 0.20  # Default: 0.15
```

---

## = Troubleshooting

### Kamera tidak terdeteksi

```python
# Edit config.py dan ubah device_id
class CameraConfig:
    device_id: int = 1  # Coba 0, 1, 2, dll.
```

### Error MediaPipe

Pastikan Anda menggunakan Python 3.12:

```bash
python --version  # Harus menampilkan Python 3.12.x
```

### Performa lambat

1. Tutup aplikasi lain yang menggunakan kamera
2. Kurangi resolusi kamera di `config.py`
3. Turunkan FPS kamera

### Error dependencies

```bash
# Instal ulang dependencies
pip install --upgrade -r requirements.txt
```

---

## =h

=� Pengembang

**Beyza Tanriverdi**

- =� Email: tnrvrd.beyza@gmail.com
- = [GitHub](https://github.com/beyzatanriverdi)
- = [LinkedIn](https://www.linkedin.com/in/beyza-tanr1verdi-8a46b0364)

**Kadir Talha Uncu**

- =� Email: talhauncu.dev@gmail.com
- = [GitHub](https://github.com/talhauncu)
- = [LinkedIn](https://www.linkedin.com/in/kadir-talha-uncu-622186339)

---

## Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file LICENSE untuk detail.

---

## Kontribusi

Kontribusi, issues, dan feature requests sangat diterima!

1. Fork proyek ini
2. Buat branch fitur Anda (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan Anda (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

---

## Ucapan Terima Kasih

- [MediaPipe](https://mediapipe.dev/) - Framework machine learning Google
- [OpenCV](https://opencv.org/) - Library computer vision
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - Framework GUI Python

---

<div align="center">

**Dibuat dengan d oleh Beyza Tanriverdi & Kadir Talha Uncu**

P Jika proyek ini membantu Anda, berikan star!

</div>
