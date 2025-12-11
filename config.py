"""
Configuration management for Monkey Pose Mimic
Centralized settings for the application
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Final


@dataclass(frozen=True)
class CameraConfig:
    """Camera configuration settings"""
    width: int = 640
    height: int = 480
    fps: int = 40
    device_id: int = 0
    flip_horizontal: bool = True


@dataclass(frozen=True)
class PoseDetectionConfig:
    """MediaPipe pose detection settings"""
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5
    model_complexity: int = 1
    smooth_landmarks: bool = True

    # Pose thresholds
    hand_raise_threshold: float = 0.05
    mouth_open_threshold: float = 0.15
    hand_to_face_threshold: float = 0.08


@dataclass(frozen=True)
class HandDetectionConfig:
    """MediaPipe hand detection settings"""
    max_num_hands: int = 2
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5
    model_complexity: int = 1


@dataclass(frozen=True)
class FaceDetectionConfig:
    """MediaPipe face mesh settings"""
    max_num_faces: int = 1
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5
    refine_landmarks: bool = True


@dataclass(frozen=True)
class UIConfig:
    """User interface configuration - macOS style"""
    window_title: str = "Monkey Pose Mimic"
    window_width: int = 1280
    window_height: int = 720
    window_pos_x: int = 100
    window_pos_y: int = 100

    # Camera display
    camera_min_width: int = 640
    camera_min_height: int = 480

    # Monkey display
    monkey_min_width: int = 480
    monkey_min_height: int = 480

    # macOS-inspired colors
    bg_color: str = "#F5F5F7"
    secondary_bg: str = "#FFFFFF"
    border_color: str = "#E5E5E7"
    text_color: str = "#1D1D1F"
    secondary_text: str = "#86868B"
    accent_color: str = "#007AFF"
    success_color: str = "#34C759"
    warning_color: str = "#FF9500"

    # Layout
    layout_spacing: int = 20
    layout_margin: int = 20
    border_radius: int = 12
    shadow_blur: int = 20


@dataclass(frozen=True)
class AssetConfig:
    """Asset file paths"""
    base_dir: Path = Path("assets")

    @property
    def raising_hand(self) -> Path:
        return self.base_dir / "raising_hand_pose.jpg"

    @property
    def shocking(self) -> Path:
        return self.base_dir / "shocking_pose.jpg"

    @property
    def thinking(self) -> Path:
        return self.base_dir / "thinking_pose.jpg"

    @property
    def default(self) -> Path:
        return self.base_dir / "default_pose.jpg"


@dataclass(frozen=True)
class AppConfig:
    """Main application configuration"""
    camera: CameraConfig = CameraConfig()
    pose: PoseDetectionConfig = PoseDetectionConfig()
    hands: HandDetectionConfig = HandDetectionConfig()
    face: FaceDetectionConfig = FaceDetectionConfig()
    ui: UIConfig = UIConfig()
    assets: AssetConfig = AssetConfig()

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Debug mode
    show_debug_info: bool = True
    show_landmarks: bool = True
    
    # Default language
    default_language: str = "id"  # Indonesian as default


# Pose name mappings - Indonesian (default)
POSE_NAMES_ID: Final[dict[str, str]] = {
    "raising_hand": "👋 Mengangkat Tangan",
    "shocking": "😲 Terkejut (Mulut Terbuka)",
    "thinking": "🤔 Berpikir (Tangan di Wajah)",
    "default": "🙂 Posisi Normal"
}

# English
POSE_NAMES_EN: Final[dict[str, str]] = {
    "raising_hand": "👋 Raising Hand",
    "shocking": "😲 Shocking (Open Mouth)",
    "thinking": "🤔 Thinking (Hand on Face)",
    "default": "🙂 Default Pose"
}

# Turkish
POSE_NAMES_TR: Final[dict[str, str]] = {
    "raising_hand": "👋 İşaret Parmağı Yukarıda",
    "shocking": "😲 Ağız Açık (Şaşkınlık)",
    "thinking": "🤔 El Yüzde (Düşünme)",
    "default": "🙂 Normal Duruş"
}

# UI text translations
UI_TEXT: Final[dict[str, dict[str, str]]] = {
    "id": {
        "camera_title": "📷 Kamera Langsung",
        "monkey_title": "🐵 Pose Monyet",
        "language": "Bahasa:",
        "show_landmarks": "Tampilkan Garis Deteksi",
        "hide_landmarks": "Sembunyikan Garis Deteksi",
        "settings": "⚙️ Pengaturan",
        "hands": "Tangan",
        "face": "Wajah",
        "mouth": "Mulut",
        "hand_height": "Tinggi Tangan",
        "pose": "Pose",
        "yes": "YA",
        "no": "TIDAK"
    },
    "en": {
        "camera_title": "📷 Live Camera",
        "monkey_title": "🐵 Monkey Pose",
        "language": "Language:",
        "show_landmarks": "Show Detection Lines",
        "hide_landmarks": "Hide Detection Lines",
        "settings": "⚙️ Settings",
        "hands": "Hands",
        "face": "Face",
        "mouth": "Mouth",
        "hand_height": "Hand Height",
        "pose": "Pose",
        "yes": "YES",
        "no": "NO"
    },
    "tr": {
        "camera_title": "📷 Canlı Kamera",
        "monkey_title": "🐵 Maymun Pozu",
        "language": "Dil:",
        "show_landmarks": "Algılama Çizgilerini Göster",
        "hide_landmarks": "Algılama Çizgilerini Gizle",
        "settings": "⚙️ Ayarlar",
        "hands": "Eller",
        "face": "Yüz",
        "mouth": "Ağız",
        "hand_height": "El Yüksekliği",
        "pose": "Poz",
        "yes": "EVET",
        "no": "HAYIR"
    }
}

# Language options
LANGUAGES: Final[dict[str, str]] = {
    "id": "🇮🇩 Bahasa Indonesia",
    "en": "🇬🇧 English",
    "tr": "🇹🇷 Türkçe"
}

# Global config instance
CONFIG: Final[AppConfig] = AppConfig()