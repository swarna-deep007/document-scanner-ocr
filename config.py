"""
Configuration settings for Document Scanner & OCR
"""

# ================== TESSERACT CONFIGURATION ==================
# Path to Tesseract executable
# Update this if Tesseract is installed in a different location
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Alternative paths to check (if default doesn't work)
TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\91743\AppData\Local\Tesseract-OCR\tesseract.exe',
]

# ================== OCR SETTINGS ==================
# Default OCR language
DEFAULT_LANGUAGE = 'eng'

# Tesseract PSM (Page Segmentation Mode)
# 1: Automatic page segmentation with OSD
# 3: Fully automatic page segmentation (default)
# 6: Uniform block of text
# 11: Sparse text
# 13: Raw text
DEFAULT_PSM = 3

# ================== IMAGE PROCESSING ==================
# Default preprocessing method
# Options: 'adaptive', 'otsu', 'clahe', 'morphological', 'denoise'
DEFAULT_PREPROCESSING = 'adaptive'

# Image resize height for faster processing
PROCESSING_HEIGHT = 500

# Canny edge detection parameters
CANNY_THRESHOLD_1 = 75
CANNY_THRESHOLD_2 = 200

# Contour approximation tolerance (percentage of perimeter)
CONTOUR_APPROXIMATION_TOLERANCE = 0.02

# Number of top contours to consider
TOP_CONTOURS_COUNT = 5

# ================== PREPROCESSING PARAMETERS ==================
# Adaptive Thresholding
ADAPTIVE_BLOCK_SIZE = 11
ADAPTIVE_C = 2

# CLAHE
CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_SIZE = (8, 8)

# Gaussian Blur
GAUSSIAN_BLUR_SIZE = (5, 5)
GAUSSIAN_BLUR_SIGMA = 0

# Morphological Operations
MORPH_KERNEL_SIZE = (3, 3)

# Denoising
DENOISE_H = 10
DENOISE_TEMPLATE_WINDOW_SIZE = 7
DENOISE_SEARCH_WINDOW_SIZE = 21

# ================== FILE HANDLING ==================
# Supported image extensions
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

# Upload folder for web app
UPLOAD_FOLDER = 'uploads'

# Processed images folder
PROCESSED_FOLDER = 'processed_images'

# Output folder
OUTPUT_FOLDER = 'output'

# Maximum file size (16 MB)
MAX_FILE_SIZE = 16 * 1024 * 1024

# ================== WEB INTERFACE ==================
# Flask server settings
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = False

# ================== LOGGING ==================
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'

# Log messages
VERBOSE = True

# ================== PERFORMANCE ==================
# Enable/disable processing history
SAVE_PROCESSING_HISTORY = True

# Number of worker threads for batch processing
WORKER_THREADS = 2

# ================== DEBUG ==================
# Debug mode (enables additional visualizations)
DEBUG_MODE = False

# Show intermediate images
SHOW_INTERMEDIATE_IMAGES = False
