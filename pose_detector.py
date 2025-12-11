from __future__ import annotations

import logging
from typing import Optional, Tuple
from dataclasses import dataclass

import cv2
import mediapipe as mp
import numpy as np
import numpy.typing as npt

from config import CONFIG, UI_TEXT

logger = logging.getLogger(__name__)


@dataclass
class DebugInfo:
    """Debug information for pose detection"""
    mouth_ratio: float = 0.0
    hand_height: float = 0.0
    hands_detected: int = 0
    face_detected: bool = False


class PoseDetector:
    """
    MediaPipe-based pose detector supporting 4 poses:
    - Raising hand
    - Shocking (mouth open)
    - Thinking (hand on face)
    - Default
    """

    def __init__(self) -> None:
        """Initialize MediaPipe models and configurations"""
        logger.info("Initializing PoseDetector...")

        # MediaPipe modules
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh

        try:
            self.pose = self.mp_pose.Pose(
                static_image_mode=False,
                model_complexity=CONFIG.pose.model_complexity,
                smooth_landmarks=CONFIG.pose.smooth_landmarks,
                min_detection_confidence=CONFIG.pose.min_detection_confidence,
                min_tracking_confidence=CONFIG.pose.min_tracking_confidence,
            )

            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=CONFIG.hands.max_num_hands,
                model_complexity=CONFIG.hands.model_complexity,
                min_detection_confidence=CONFIG.hands.min_detection_confidence,
                min_tracking_confidence=CONFIG.hands.min_tracking_confidence,
            )

            self.face_mesh = self.mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=CONFIG.face.max_num_faces,
                refine_landmarks=CONFIG.face.refine_landmarks,
                min_detection_confidence=CONFIG.face.min_detection_confidence,
                min_tracking_confidence=CONFIG.face.min_tracking_confidence,
            )

            logger.info("MediaPipe models initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MediaPipe models: {e}")
            raise

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Debug information
        self.debug_info = DebugInfo()
        
        # Current language for debug display
        self.current_language = CONFIG.default_language

    def detect_pose(
        self, 
        frame: npt.NDArray[np.uint8],
        show_landmarks: bool = True,
        language: str = "id"
    ) -> Tuple[npt.NDArray[np.uint8], str]:
        """
        Perform pose detection on a video frame

        Args:
            frame: BGR video frame from OpenCV
            show_landmarks: Whether to draw landmark lines on the frame
            language: Current language for debug info

        Returns:
            Tuple of (processed_frame, pose_name)
        """
        self.current_language = language
        
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            logger.error(f"Failed to convert frame to RGB: {e}")
            return frame, "default"

        # ALWAYS run detections - regardless of show_landmarks setting
        # This ensures pose detection works even when landmarks are hidden
        try:
            pose_results = self.pose.process(rgb_frame)
            hand_results = self.hands.process(rgb_frame)
            face_results = self.face_mesh.process(rgb_frame)
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return frame, "default"

        # Reset debug info
        self.debug_info = DebugInfo()

        # Update debug info
        try:
            if face_results and face_results.multi_face_landmarks:
                self.debug_info.face_detected = True
            
            if hand_results and hand_results.multi_hand_landmarks:
                self.debug_info.hands_detected = len(hand_results.multi_hand_landmarks)
        except Exception as e:
            logger.error(f"Failed to update debug info: {e}")

        # Determine pose BEFORE drawing (so it works regardless of landmark visibility)
        pose_name = self._determine_pose(pose_results, hand_results, face_results)

        # Only draw landmarks if enabled
        if show_landmarks:
            # Create a copy of the frame for drawing
            display_frame = frame.copy()
            
            try:
                # Draw face landmarks (lips only)
                if face_results and face_results.multi_face_landmarks:
                    for face_landmarks in face_results.multi_face_landmarks:
                        self.mp_drawing.draw_landmarks(
                            display_frame,
                            face_landmarks,
                            self.mp_face_mesh.FACEMESH_LIPS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=self.mp_drawing.DrawingSpec(
                                color=(0, 255, 255), thickness=1
                            ),
                        )

                # Draw hand landmarks
                if hand_results and hand_results.multi_hand_landmarks:
                    for hand_landmarks in hand_results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            display_frame,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style(),
                        )
            except Exception as e:
                logger.error(f"Failed to draw landmarks: {e}")

            # Show debug information if enabled
            if CONFIG.show_debug_info:
                self._draw_debug_info(display_frame, pose_name)
            
            return display_frame, pose_name
        else:
            # Return original frame without any drawings
            return frame, pose_name

    def _draw_debug_info(self, frame: npt.NDArray[np.uint8], pose_name: str) -> None:
        """Draw debug information on the frame"""
        ui_text = UI_TEXT.get(self.current_language, UI_TEXT["id"])
        
        y_pos = 30
        
        # Semi-transparent background for debug text
        overlay = frame.copy()
        cv2.rectangle(overlay, (5, 10), (280, 180), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        cv2.putText(
            frame,
            f"{ui_text['hands']}: {self.debug_info.hands_detected}",
            (10, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2,
        )
        y_pos += 30
        cv2.putText(
            frame,
            f"{ui_text['face']}: {ui_text['yes'] if self.debug_info.face_detected else ui_text['no']}",
            (10, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2,
        )
        y_pos += 30
        cv2.putText(
            frame,
            f"{ui_text['mouth']}: {self.debug_info.mouth_ratio:.3f}",
            (10, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2,
        )
        y_pos += 30
        cv2.putText(
            frame,
            f"{ui_text['hand_height']}: {self.debug_info.hand_height:.3f}",
            (10, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2,
        )

        # Show pose name at bottom with background
        text = f"{ui_text['pose']}: {pose_name}"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_x = 10
        text_y = frame.shape[0] - 20
        
        # Background for pose text
        overlay = frame.copy()
        cv2.rectangle(
            overlay, 
            (text_x - 5, text_y - text_size[1] - 5), 
            (text_x + text_size[0] + 5, text_y + 5), 
            (0, 0, 0), 
            -1
        )
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        cv2.putText(
            frame,
            text,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )
    
    def _determine_pose(
        self,
        pose_results: Optional[mp.solutions.pose.Pose],
        hand_results: Optional[mp.solutions.hands.Hands],
        face_results: Optional[mp.solutions.face_mesh.FaceMesh],
    ) -> str:
        """
        Determine pose from detection results
        Priority: raising_hand > thinking > shocking > default
        """
        if self._is_raising_hand(pose_results, hand_results):
            return "raising_hand"

        if self._is_thinking(pose_results, hand_results, face_results):
            return "thinking"

        if self._is_shocking(face_results):
            return "shocking"

        return "default"

    def _is_raising_hand(
        self,
        pose_results: Optional[mp.solutions.pose.Pose],
        hand_results: Optional[mp.solutions.hands.Hands],
    ) -> bool:
        """Check if hand is raised above head level"""
        if not pose_results or not hand_results:
            self.debug_info.hand_height = 0.0
            return False
            
        if not pose_results.pose_landmarks or not hand_results.multi_hand_landmarks:
            self.debug_info.hand_height = 0.0
            return False

        pose_landmarks = pose_results.pose_landmarks.landmark
        nose_y = pose_landmarks[self.mp_pose.PoseLandmark.NOSE].y

        for hand_landmarks in hand_results.multi_hand_landmarks:
            wrist_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y
            height_diff = nose_y - wrist_y
            self.debug_info.hand_height = height_diff

            if height_diff > CONFIG.pose.hand_raise_threshold:
                return True

        return False

    def _is_shocking(
        self, face_results: Optional[mp.solutions.face_mesh.FaceMesh]
    ) -> bool:
        """Check if mouth is open (shocking pose)"""
        if not face_results:
            self.debug_info.mouth_ratio = 0.0
            return False
            
        if not face_results.multi_face_landmarks:
            self.debug_info.mouth_ratio = 0.0
            return False

        try:
            face_landmarks = face_results.multi_face_landmarks[0].landmark

            # Mouth landmarks
            upper_lip = face_landmarks[13].y
            lower_lip = face_landmarks[14].y
            forehead = face_landmarks[10].y
            chin = face_landmarks[152].y
            face_height = abs(chin - forehead)

            mouth_opening = abs(lower_lip - upper_lip)
            mouth_ratio = mouth_opening / face_height if face_height > 0 else 0
            self.debug_info.mouth_ratio = mouth_ratio

            return mouth_ratio > CONFIG.pose.mouth_open_threshold
        except (IndexError, AttributeError) as e:
            logger.error(f"Error checking shocking pose: {e}")
            self.debug_info.mouth_ratio = 0.0
            return False

    def _is_thinking(
        self,
        pose_results: Optional[mp.solutions.pose.Pose],
        hand_results: Optional[mp.solutions.hands.Hands],
        face_results: Optional[mp.solutions.face_mesh.FaceMesh],
    ) -> bool:
        """Check if hand is touching face (thinking pose)"""
        if not face_results or not hand_results:
            return False
            
        if not face_results.multi_face_landmarks or not hand_results.multi_hand_landmarks:
            return False

        try:
            face_landmarks = face_results.multi_face_landmarks[0].landmark

            # Mouth region landmarks
            mouth_points = [
                face_landmarks[13],  # Upper lip
                face_landmarks[14],  # Lower lip
                face_landmarks[152],  # Chin
                face_landmarks[0],  # Mouth center
            ]

            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Finger tips
                finger_tips = [
                    hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP],
                    hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP],
                    hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                ]

                # Check if any finger is close to mouth region
                for finger_tip in finger_tips:
                    for mouth_point in mouth_points:
                        distance = np.sqrt(
                            (finger_tip.x - mouth_point.x) ** 2
                            + (finger_tip.y - mouth_point.y) ** 2
                        )

                        if distance < CONFIG.pose.hand_to_face_threshold:
                            return True

            return False
        except (IndexError, AttributeError) as e:
            logger.error(f"Error checking thinking pose: {e}")
            return False

    def release(self) -> None:
        """Release MediaPipe resources"""
        logger.info("Releasing PoseDetector resources...")
        try:
            self.pose.close()
            self.hands.close()
            self.face_mesh.close()
            logger.info("Resources released successfully")
        except Exception as e:
            logger.error(f"Error releasing resources: {e}")