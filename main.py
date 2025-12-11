"""
Monkey Pose Mimic - Main Application
PyQt5 GUI + MediaPipe pose detection with macOS-inspired design
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Dict, Optional

import cv2
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QPushButton,
    QCheckBox,
    QFrame,
)

from config import CONFIG, POSE_NAMES_ID, POSE_NAMES_EN, POSE_NAMES_TR, UI_TEXT, LANGUAGES

# Setup logging
logging.basicConfig(
    level=getattr(logging, CONFIG.log_level),
    format=CONFIG.log_format,
)
logger = logging.getLogger(__name__)

# Import pose detector with error handling
try:
    from pose_detector import PoseDetector

    logger.info("MediaPipe pose detection initialized!")
except ImportError as e:
    logger.critical(f"Failed to import pose_detector: {e}")
    print("=" * 60)
    print("ERROR: MediaPipe not found!")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print()
    print("MediaPipe only works with Python 3.12 and below.")
    print("If you're using Python 3.13:")
    print()
    print("1. Install Python 3.12:")
    print("   https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe")
    print()
    print("2. Run with this command:")
    print("   py -3.12 main.py")
    print()
    print("=" * 60)
    sys.exit(1)


class MonkeyPoseApp(QMainWindow):
    """Main application window for Monkey Pose Mimic - macOS style"""

    def __init__(self) -> None:
        """Initialize the application window"""
        super().__init__()
        logger.info("Initializing MonkeyPoseApp...")

        # Current language
        self.current_language = CONFIG.default_language
        
        # Landmark visibility
        self.show_landmarks = CONFIG.show_landmarks

        # Window configuration
        self.setWindowTitle(CONFIG.ui.window_title)
        self.setGeometry(
            CONFIG.ui.window_pos_x,
            CONFIG.ui.window_pos_y,
            CONFIG.ui.window_width,
            CONFIG.ui.window_height,
        )
        
        # macOS-inspired stylesheet
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {CONFIG.ui.bg_color};
            }}
            QLabel {{
                color: {CONFIG.ui.text_color};
            }}
            QComboBox {{
                background-color: {CONFIG.ui.secondary_bg};
                border: 1px solid {CONFIG.ui.border_color};
                border-radius: 8px;
                padding: 8px 12px;
                color: {CONFIG.ui.text_color};
                font-size: 13px;
                min-width: 180px;
            }}
            QComboBox:hover {{
                border: 1px solid {CONFIG.ui.accent_color};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {CONFIG.ui.text_color};
                margin-right: 5px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {CONFIG.ui.secondary_bg};
                border: 1px solid {CONFIG.ui.border_color};
                border-radius: 8px;
                selection-background-color: {CONFIG.ui.accent_color};
                selection-color: white;
                padding: 4px;
            }}
            QPushButton {{
                background-color: {CONFIG.ui.accent_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #0051D5;
            }}
            QPushButton:pressed {{
                background-color: #004FC4;
            }}
            QCheckBox {{
                color: {CONFIG.ui.text_color};
                font-size: 13px;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 1px solid {CONFIG.ui.border_color};
                background-color: {CONFIG.ui.secondary_bg};
            }}
            QCheckBox::indicator:checked {{
                background-color: {CONFIG.ui.accent_color};
                border: 1px solid {CONFIG.ui.accent_color};
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEzLjMzMzMgNEw2IDExLjMzMzNMMi42NjY2NyA4IiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }}
            QCheckBox::indicator:hover {{
                border: 1px solid {CONFIG.ui.accent_color};
            }}
        """)

        # Initialize camera
        self.camera: Optional[cv2.VideoCapture] = None
        self._init_camera()

        # Initialize pose detector
        try:
            self.pose_detector = PoseDetector()
        except Exception as e:
            logger.error(f"Failed to initialize PoseDetector: {e}")
            raise

        # Load monkey images
        self.monkey_images: Dict[str, Optional[str]] = self._load_monkey_images()
        self.current_pose: str = "default"

        # UI elements
        self.camera_label: Optional[QLabel] = None
        self.monkey_label: Optional[QLabel] = None
        self.pose_name_label: Optional[QLabel] = None
        self.language_combo: Optional[QComboBox] = None
        self.landmark_checkbox: Optional[QCheckBox] = None
        self.camera_title: Optional[QLabel] = None
        self.monkey_title: Optional[QLabel] = None

        # Setup UI
        self._setup_ui()

        # Timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        fps_interval = int(1000 / CONFIG.camera.fps)
        self.timer.start(fps_interval)

        logger.info("MonkeyPoseApp initialized successfully")

    def _init_camera(self) -> None:
        """Initialize camera with error handling"""
        try:
            self.camera = cv2.VideoCapture(CONFIG.camera.device_id)
            if not self.camera.isOpened():
                raise RuntimeError("Failed to open camera")

            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG.camera.width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG.camera.height)
            logger.info(
                f"Camera initialized: {CONFIG.camera.width}x{CONFIG.camera.height}"
            )
        except Exception as e:
            logger.error(f"Camera initialization failed: {e}")
            raise
    
    def _setup_ui(self) -> None:
        """Setup the user interface with macOS styling"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar with settings
        top_bar = self._create_top_bar()
        main_layout.addWidget(top_bar)
        
        # Content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(CONFIG.ui.layout_spacing)
        content_layout.setContentsMargins(
            CONFIG.ui.layout_margin,
            CONFIG.ui.layout_margin,
            CONFIG.ui.layout_margin,
            CONFIG.ui.layout_margin,
        )
        
        # Left - Camera
        left_layout = self._create_camera_section()
        
        # Right - Monkey
        right_layout = self._create_monkey_section()

        content_layout.addLayout(left_layout, 60)
        content_layout.addLayout(right_layout, 40)
        
        main_layout.addLayout(content_layout)

        self._update_monkey_image("default")

    def _create_top_bar(self) -> QWidget:
        """Create top bar with language selector and settings"""
        top_bar = QFrame()
        top_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {CONFIG.ui.secondary_bg};
                border-bottom: 1px solid {CONFIG.ui.border_color};
            }}
        """)
        top_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Language selector
        lang_label = QLabel(UI_TEXT[self.current_language]["language"])
        lang_label.setStyleSheet(f"color: {CONFIG.ui.secondary_text}; font-size: 13px; border: none;")
        
        self.language_combo = QComboBox()
        for lang_code, lang_name in LANGUAGES.items():
            self.language_combo.addItem(lang_name, lang_code)
        
        # Set current language
        current_index = list(LANGUAGES.keys()).index(self.current_language)
        self.language_combo.setCurrentIndex(current_index)
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        
        # Landmark toggle
        self.landmark_checkbox = QCheckBox(
            UI_TEXT[self.current_language]["show_landmarks" if self.show_landmarks else "hide_landmarks"]
        )
        self.landmark_checkbox.setChecked(self.show_landmarks)
        self.landmark_checkbox.stateChanged.connect(self._on_landmark_toggle)
        
        layout.addWidget(lang_label)
        layout.addWidget(self.language_combo)
        layout.addSpacing(20)
        layout.addWidget(self.landmark_checkbox)
        layout.addStretch()
        
        return top_bar

    def _create_camera_section(self) -> QVBoxLayout:
        """Create camera display section"""
        layout = QVBoxLayout()
        
        self.camera_title = QLabel(UI_TEXT[self.current_language]["camera_title"])
        self.camera_title.setFont(QFont("SF Pro Display", 18, QFont.Weight.Bold))
        self.camera_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.camera_title.setStyleSheet(f"""
            QLabel {{
                color: {CONFIG.ui.text_color};
                background: transparent;
                border: none;
                padding: 10px 0px;
            }}
        """)
        
        # Camera container with shadow effect
        camera_container = QFrame()
        camera_container.setStyleSheet(f"""
            QFrame {{
                background-color: {CONFIG.ui.secondary_bg};
                border-radius: {CONFIG.ui.border_radius}px;
                border: 1px solid {CONFIG.ui.border_color};
            }}
        """)
        
        camera_layout = QVBoxLayout(camera_container)
        camera_layout.setContentsMargins(0, 0, 0, 0)
        
        self.camera_label = QLabel()
        self.camera_label.setMinimumSize(
            CONFIG.ui.camera_min_width, CONFIG.ui.camera_min_height
        )
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setScaledContents(True)
        self.camera_label.setStyleSheet(f"""
            QLabel {{
                background-color: #000;
                border-radius: {CONFIG.ui.border_radius}px;
                border: none;
            }}
        """)
        
        camera_layout.addWidget(self.camera_label)
        
        layout.addWidget(self.camera_title)
        layout.addWidget(camera_container)
        layout.setSpacing(10)
        
        return layout

    def _create_monkey_section(self) -> QVBoxLayout:
        """Create monkey display section"""
        layout = QVBoxLayout()
        
        self.monkey_title = QLabel(UI_TEXT[self.current_language]["monkey_title"])
        self.monkey_title.setFont(QFont("SF Pro Display", 18, QFont.Weight.Bold))
        self.monkey_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.monkey_title.setStyleSheet(f"""
            QLabel {{
                color: {CONFIG.ui.text_color};
                background: transparent;
                border: none;
                padding: 10px 0px;
            }}
        """)
        
        # Monkey container
        monkey_container = QFrame()
        monkey_container.setStyleSheet(f"""
            QFrame {{
                background-color: {CONFIG.ui.secondary_bg};
                border-radius: {CONFIG.ui.border_radius}px;
                border: 1px solid {CONFIG.ui.border_color};
            }}
        """)
        
        monkey_layout = QVBoxLayout(monkey_container)
        monkey_layout.setContentsMargins(0, 0, 0, 0)
        monkey_layout.setSpacing(0)
        
        self.monkey_label = QLabel()
        self.monkey_label.setMinimumSize(
            CONFIG.ui.monkey_min_width, CONFIG.ui.monkey_min_height
        )
        self.monkey_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monkey_label.setScaledContents(True)
        self.monkey_label.setStyleSheet(f"""
            QLabel {{
                background-color: {CONFIG.ui.secondary_bg};
                border-radius: {CONFIG.ui.border_radius}px {CONFIG.ui.border_radius}px 0px 0px;
                border: none;
            }}
        """)
        
        # Pose name label
        self.pose_name_label = QLabel("Normal Pose")
        self.pose_name_label.setFont(QFont("SF Pro Display", 16, QFont.Weight.Medium))
        self.pose_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pose_name_label.setStyleSheet(f"""
            QLabel {{
                color: {CONFIG.ui.accent_color};
                background-color: {CONFIG.ui.bg_color};
                border: none;
                border-radius: 0px 0px {CONFIG.ui.border_radius}px {CONFIG.ui.border_radius}px;
                padding: 15px;
            }}
        """)
        
        monkey_layout.addWidget(self.monkey_label, 1)
        monkey_layout.addWidget(self.pose_name_label, 0)
        
        layout.addWidget(self.monkey_title)
        layout.addWidget(monkey_container)
        layout.setSpacing(10)
        
        return layout

    def _on_language_changed(self, index: int) -> None:
        """Handle language change"""
        lang_code = self.language_combo.itemData(index)
        self.current_language = lang_code
        logger.info(f"Language changed to: {lang_code}")
        
        # Update UI text
        if self.camera_title:
            self.camera_title.setText(UI_TEXT[lang_code]["camera_title"])
        if self.monkey_title:
            self.monkey_title.setText(UI_TEXT[lang_code]["monkey_title"])
        if self.landmark_checkbox:
            self.landmark_checkbox.setText(
                UI_TEXT[lang_code]["show_landmarks" if self.show_landmarks else "hide_landmarks"]
            )
        
        # Update pose name
        self._update_pose_name_display()

    def _on_landmark_toggle(self, state: int) -> None:
        """Handle landmark visibility toggle"""
        self.show_landmarks = state == Qt.CheckState.Checked
        logger.info(f"Landmarks visibility: {self.show_landmarks}")
        
        # Update checkbox text
        if self.landmark_checkbox:
            self.landmark_checkbox.setText(
                UI_TEXT[self.current_language]["show_landmarks" if self.show_landmarks else "hide_landmarks"]
            )

    def _update_pose_name_display(self) -> None:
        """Update pose name based on current language"""
        if not self.pose_name_label:
            return
            
        pose_names = {
            "id": POSE_NAMES_ID,
            "en": POSE_NAMES_EN,
            "tr": POSE_NAMES_TR
        }
        
        current_names = pose_names.get(self.current_language, POSE_NAMES_ID)
        self.pose_name_label.setText(current_names.get(self.current_pose, self.current_pose))

    def _load_monkey_images(self) -> Dict[str, Optional[str]]:
        """Load monkey pose images from assets folder"""
        images: Dict[str, Optional[str]] = {}
        pose_paths = {
            "raising_hand": CONFIG.assets.raising_hand,
            "shocking": CONFIG.assets.shocking,
            "thinking": CONFIG.assets.thinking,
            "default": CONFIG.assets.default,
        }

        for pose, image_path in pose_paths.items():
            if image_path.exists():
                images[pose] = str(image_path)
                logger.info(f"Loaded image for pose '{pose}': {image_path}")
            else:
                logger.warning(f"Image not found for pose '{pose}': {image_path}")
                images[pose] = None

        return images

    def _update_frame(self) -> None:
        """Update camera frame and detect pose"""
        if not self.camera or not self.camera.isOpened():
            logger.error("Camera not available")
            return

        ret, frame = self.camera.read()
        if not ret:
            logger.warning("Failed to read frame from camera")
            return

        # Flip horizontally for mirror effect
        if CONFIG.camera.flip_horizontal:
            frame = cv2.flip(frame, 1)
        
        # Pose detection with landmark visibility control
        processed_frame, pose_name = self.pose_detector.detect_pose(
            frame, 
            show_landmarks=self.show_landmarks,
            language=self.current_language
        )

        # Display camera feed
        try:
            rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            qt_image = QImage(
                rgb_frame.data, w, h, ch * w, QImage.Format.Format_RGB888
            )

            pixmap = QPixmap.fromImage(qt_image)
            if self.camera_label:
                self.camera_label.setPixmap(pixmap)
        except Exception as e:
            logger.error(f"Failed to display frame: {e}")
            return

        # Update monkey image if pose changed
        if pose_name != self.current_pose:
            self.current_pose = pose_name
            self._update_monkey_image(pose_name)

    def _update_monkey_image(self, pose_name: str) -> None:
        """Update monkey image based on detected pose"""
        if not self.monkey_label or not self.pose_name_label:
            return

        image_path = self.monkey_images.get(pose_name)

        if image_path:
            pixmap = QPixmap(image_path)
            self.monkey_label.setPixmap(pixmap)
            logger.debug(f"Updated monkey image to pose: {pose_name}")
        else:
            self.monkey_label.setText(f"{pose_name}\n\n(Image not found)")
            self.monkey_label.setStyleSheet(f"""
                QLabel {{ 
                    color: {CONFIG.ui.warning_color}; 
                    font-size: 16px; 
                    border: 2px dashed {CONFIG.ui.border_color}; 
                }}
            """)
            logger.warning(f"No image found for pose: {pose_name}")

        self._update_pose_name_display()

    def closeEvent(self, event) -> None:  # type: ignore
        """Cleanup resources on application close"""
        logger.info("Closing application...")
        self.timer.stop()

        if self.camera:
            self.camera.release()
            logger.info("Camera released")

        self.pose_detector.release()

        event.accept()
        logger.info("Application closed successfully")


def main() -> None:
    """Main entry point for the application"""
    logger.info("Starting Monkey Pose Mimic application...")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        window = MonkeyPoseApp()
        window.show()
        logger.info("Application window displayed")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()