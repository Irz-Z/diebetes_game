#!/usr/bin/env python3
"""
Road Crack Detection System
Processes video files to detect and calculate crack areas with robust error handling.
"""

import cv2
import numpy as np
import sys
import os
import time
import logging
from pathlib import Path
import argparse
from typing import Optional, Tuple, List, Any
import traceback

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class VideoProcessor:
    """Robust video processor with error handling and multiple backend support."""
    
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = None
        self.total_frames = 0
        self.fps = 0
        self.frame_width = 0
        self.frame_height = 0
        self.backends = [cv2.CAP_FFMPEG, cv2.CAP_DSHOW, cv2.CAP_ANY]
        
    def _try_open_video(self) -> bool:
        """Try opening video with different backends."""
        for backend in self.backends:
            try:
                logger.info(f"Attempting to open video with backend: {backend}")
                self.cap = cv2.VideoCapture(self.video_path, backend)
                
                if self.cap.isOpened():
                    # Get video properties
                    self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                    self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    
                    logger.info(f"Video opened successfully with backend {backend}")
                    logger.info(f"Video properties: {self.frame_width}x{self.frame_height}, "
                              f"{self.total_frames} frames, {self.fps:.2f} FPS")
                    return True
                else:
                    self.cap.release()
                    self.cap = None
                    
            except Exception as e:
                logger.warning(f"Failed to open with backend {backend}: {e}")
                if self.cap:
                    self.cap.release()
                    self.cap = None
                continue
                
        return False
    
    def validate_frame(self, frame: np.ndarray) -> bool:
        """Validate if frame is not corrupted."""
        if frame is None:
            return False
        if frame.size == 0:
            return False
        if len(frame.shape) < 2:
            return False
        # Check for reasonable frame dimensions
        if frame.shape[0] < 10 or frame.shape[1] < 10:
            return False
        return True
    
    def open(self) -> bool:
        """Open video file with error handling."""
        if not os.path.exists(self.video_path):
            logger.error(f"Video file not found: {self.video_path}")
            return False
            
        # Validate file format
        valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
        file_ext = Path(self.video_path).suffix.lower()
        if file_ext not in valid_extensions:
            logger.warning(f"Potentially unsupported video format: {file_ext}")
            
        return self._try_open_video()
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read frame with validation and error handling."""
        if not self.cap or not self.cap.isOpened():
            return False, None
            
        try:
            ret, frame = self.cap.read()
            if ret and self.validate_frame(frame):
                return True, frame
            else:
                if ret:
                    logger.warning("Frame failed validation, skipping corrupted frame")
                return False, None
        except Exception as e:
            logger.warning(f"Error reading frame: {e}")
            return False, None
    
    def release(self):
        """Release video capture resources."""
        if self.cap:
            self.cap.release()
            self.cap = None

class CrackDetector:
    """Crack detection algorithm with area calculation."""
    
    def __init__(self):
        self.total_crack_area = 0.0
        self.processed_frames = 0
        
    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Preprocess frame for crack detection."""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        return edges
    
    def detect_cracks(self, frame: np.ndarray) -> Tuple[np.ndarray, float]:
        """Detect cracks in frame and calculate area."""
        try:
            # Preprocess the frame
            edges = self.preprocess_frame(frame)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours that might be cracks (length vs area ratio)
            crack_contours = []
            frame_area = 0.0
            
            for contour in contours:
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)
                
                # Filter based on aspect ratio and minimum area
                if area > 50 and perimeter > 100:
                    # Calculate aspect ratio
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = max(w, h) / min(w, h)
                    
                    # Cracks typically have high aspect ratios
                    if aspect_ratio > 3:
                        crack_contours.append(contour)
                        frame_area += area
            
            # Draw detected cracks on frame copy
            result_frame = frame.copy()
            cv2.drawContours(result_frame, crack_contours, -1, (0, 0, 255), 2)
            
            return result_frame, frame_area
            
        except Exception as e:
            logger.error(f"Error in crack detection: {e}")
            return frame, 0.0
    
    def calculate_area_in_square_meters(self, pixel_area: float, 
                                      pixels_per_meter: float = 100.0) -> float:
        """Convert pixel area to square meters."""
        return pixel_area / (pixels_per_meter ** 2)

def format_area_output(area_m2: float) -> str:
    """Format area output with proper encoding handling."""
    try:
        # Try to use Unicode square meter symbol
        return f"{area_m2:.4f} m²"
    except UnicodeEncodeError:
        # Fallback to ASCII representation
        return f"{area_m2:.4f} m^2"

def safe_print(message: str):
    """Print message with encoding error handling."""
    try:
        print(message)
    except UnicodeEncodeError:
        # Convert problematic characters to ASCII
        ascii_message = message.encode('ascii', 'replace').decode('ascii')
        print(ascii_message)

class ProgressIndicator:
    """Progress indicator for video processing."""
    
    def __init__(self, total_frames: int):
        self.total_frames = total_frames
        self.start_time = time.time()
        
    def update(self, current_frame: int):
        """Update progress display."""
        if self.total_frames > 0:
            progress = (current_frame / self.total_frames) * 100
            elapsed_time = time.time() - self.start_time
            
            if current_frame > 0:
                eta = (elapsed_time / current_frame) * (self.total_frames - current_frame)
                eta_str = f", ETA: {eta:.1f}s"
            else:
                eta_str = ""
                
            progress_msg = f"Processing frame {current_frame}/{self.total_frames} " \
                          f"({progress:.1f}%){eta_str}"
            # Use regular print for progress updates to handle the end parameter
            try:
                print(f"\r{progress_msg}", end="")
            except UnicodeEncodeError:
                # Fallback to ASCII if Unicode fails
                ascii_msg = progress_msg.encode('ascii', 'replace').decode('ascii')
                print(f"\r{ascii_msg}", end="")

def process_video(video_path: str, output_path: Optional[str] = None) -> bool:
    """Process video to detect cracks with comprehensive error handling."""
    logger.info("Starting video processing...")
    
    # Initialize components
    processor = VideoProcessor(video_path)
    detector = CrackDetector()
    
    try:
        # Open video
        if not processor.open():
            logger.error("Failed to open video file")
            return False
            
        # Initialize progress indicator
        progress = ProgressIndicator(processor.total_frames)
        
        # Process frames
        frame_count = 0
        total_crack_area_pixels = 0.0
        
        while True:
            ret, frame = processor.read_frame()
            
            if not ret:
                # Check if we've reached the end or encountered an error
                if frame_count == 0:
                    logger.error("No frames could be read from video")
                    return False
                else:
                    logger.info("Reached end of video or skipping corrupted frames")
                    break
            
            try:
                # Detect cracks in current frame
                result_frame, crack_area = detector.detect_cracks(frame)
                total_crack_area_pixels += crack_area
                
                # Update progress
                frame_count += 1
                progress.update(frame_count)
                
                # Optional: Save processed frame
                if output_path and frame_count % 30 == 0:  # Save every 30th frame
                    output_frame_path = f"{output_path}_frame_{frame_count:06d}.jpg"
                    cv2.imwrite(output_frame_path, result_frame)
                
            except Exception as e:
                logger.warning(f"Error processing frame {frame_count}: {e}")
                # Continue with next frame
                continue
        
        print()  # New line after progress indicator
        
        # Calculate final results
        area_m2 = detector.calculate_area_in_square_meters(total_crack_area_pixels)
        
        # Output results with proper encoding
        safe_print(f"\n=== Processing Complete ===")
        safe_print(f"Total frames processed: {frame_count}")
        safe_print(f"Total crack area: {format_area_output(area_m2)}")
        safe_print(f"Average crack area per frame: {format_area_output(area_m2 / max(frame_count, 1))}")
        
        logger.info("Video processing completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Critical error during video processing: {e}")
        logger.error(traceback.format_exc())
        return False
        
    finally:
        processor.release()

def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(description="Road Crack Detection System")
    parser.add_argument("video_path", help="Path to input video file")
    parser.add_argument("-o", "--output", help="Output path for processed frames")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Set UTF-8 encoding for stdout if possible
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        logger.warning("Could not set UTF-8 encoding for stdout")
    
    try:
        success = process_video(args.video_path, args.output)
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        safe_print("\nProcessing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()