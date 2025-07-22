# Road Crack Detection System

A robust video processing system for detecting and measuring road cracks with comprehensive error handling and Unicode support.

## Features

### Video Processing
- **Multiple Backend Support**: Automatically tries different video backends (CAP_FFMPEG, CAP_DSHOW, CAP_ANY)
- **Robust Error Handling**: Handles h264 decoder failures and corrupted frames gracefully
- **Frame Validation**: Validates each frame before processing to skip corrupted data
- **Format Support**: Supports MP4, AVI, MOV, MKV, WMV, FLV, and WEBM formats

### Character Encoding
- **Unicode Support**: Properly displays area measurements with m² symbol
- **ASCII Fallback**: Automatically falls back to m^2 when Unicode encoding fails
- **UTF-8 Console Output**: Configures console for proper Unicode display

### User Experience
- **Real-time Progress**: Shows processing progress with frame count and ETA
- **Comprehensive Logging**: Detailed error messages and debugging information
- **Command-line Interface**: Easy-to-use CLI with help and options

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python3 calculate-crack.py input_video.mp4
```

### With Verbose Logging
```bash
python3 calculate-crack.py input_video.mp4 -v
```

### Save Processed Frames
```bash
python3 calculate-crack.py input_video.mp4 -o output_prefix
```

### Command Line Options
- `video_path`: Path to input video file (required)
- `-o, --output`: Output path prefix for saving processed frames
- `-v, --verbose`: Enable verbose logging
- `-h, --help`: Show help message

## Error Handling

The system handles various error conditions:

1. **Video Decoding Errors**: 
   - Tries multiple video backends automatically
   - Skips corrupted frames while continuing processing
   - Provides detailed error messages for debugging

2. **Character Encoding Errors**:
   - Displays Unicode m² symbol when possible
   - Falls back to ASCII m^2 when encoding fails
   - Handles console output encoding issues

3. **File Format Issues**:
   - Validates video file formats
   - Warns about potentially unsupported formats
   - Gracefully handles non-video files

## Output

The system provides:
- Real-time progress updates with ETA
- Total crack area in square meters (m² or m^2)
- Average crack area per frame
- Frame processing statistics
- Comprehensive logging information

Example output:
```
2025-07-22 14:18:40,241 - INFO - Video properties: 640x480, 150 frames, 30.00 FPS
Processing frame 150/150 (100.0%), ETA: 0.0s

=== Processing Complete ===
Total frames processed: 150
Total crack area: 1.8813 m²
Average crack area per frame: 0.0125 m²
```

## Dependencies

- `opencv-python >= 4.5.0`: Video processing and computer vision
- `numpy >= 1.19.0`: Numerical computations

## Technical Details

### Crack Detection Algorithm
The system uses edge detection and contour analysis to identify potential cracks:
1. Converts frames to grayscale
2. Applies Gaussian blur for noise reduction
3. Uses Canny edge detection
4. Filters contours based on aspect ratio and size
5. Calculates crack area in pixels and converts to square meters

### Error Recovery
- **Frame Skipping**: Continues processing when individual frames fail
- **Backend Fallback**: Tries multiple video backends if one fails
- **Encoding Fallback**: Uses ASCII alternatives when Unicode fails
- **Graceful Degradation**: Provides meaningful error messages

## Troubleshooting

### Common Issues

1. **"Video file not found"**: Check that the file path is correct
2. **"Failed to open video file"**: Video file may be corrupted or unsupported format
3. **Unicode encoding errors**: System will automatically use ASCII fallback
4. **Frame processing errors**: Individual corrupted frames are skipped automatically

### Supported Video Formats
- MP4 (recommended)
- AVI
- MOV
- MKV
- WMV
- FLV
- WEBM

For best results, use MP4 format with H.264 encoding.