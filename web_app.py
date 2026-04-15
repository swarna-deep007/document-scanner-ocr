"""
Web Interface for Document Scanner & OCR
Flask-based GUI for easy document scanning and text extraction.
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import cv2
import base64
import io
from pathlib import Path
import json
from document_scanner import DocumentScanner
import logging

# Configure Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed_images'

# Create folders
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['PROCESSED_FOLDER']).mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize scanner
scanner = DocumentScanner(debug=False)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'tiff'}


def allowed_file(filename):
    """Check if file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def image_to_base64(img_path):
    """Convert image to base64 string."""
    with open(img_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/api/scan', methods=['POST'])
def scan_document():
    """
    API endpoint to scan a document.
    
    Expected form data:
    - file: image file
    - preprocessing_method: 'adaptive', 'otsu', 'clahe', 'morphological'
    - language: OCR language
    """
    try:
        # Validate file
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400
        
        # Get parameters
        preprocessing_method = request.form.get('preprocessing_method', 'adaptive')
        language = request.form.get('language', 'eng')
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(filepath)
        
        logger.info(f"Processing file: {filename}")
        
        # Scan document
        result = scanner.scan_document(
            str(filepath),
            preprocessing_method=preprocessing_method,
            lang=language
        )
        
        if result['success']:
            # Save processed images
            output_dir = Path(app.config['PROCESSED_FOLDER']) / filename.split('.')[0]
            output_dir.mkdir(exist_ok=True)
            scanner.save_processed_images(str(output_dir))
            
            # Create base64 images for display
            images = {}
            for prefix in ['1_original', '2_warped', '3_processed']:
                img_path = output_dir / f"{prefix}.jpg"
                if img_path.exists():
                    images[prefix] = image_to_base64(str(img_path))
            
            return jsonify({
                'success': True,
                'text': result['text'],
                'images': images,
                'original_shape': result['original_shape'],
                'processed_shape': result['processed_shape']
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        logger.error(f"Error in scan_document: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/preprocessing-methods', methods=['GET'])
def get_preprocessing_methods():
    """Get available preprocessing methods."""
    methods = [
        {
            'id': 'adaptive',
            'name': 'Adaptive Thresholding',
            'description': 'Gaussian adaptive thresholding for varying lighting'
        },
        {
            'id': 'otsu',
            'name': "Otsu's Thresholding",
            'description': 'Automatic thresholding with maximum variance'
        },
        {
            'id': 'clahe',
            'name': 'CLAHE',
            'description': 'Contrast Limited Adaptive Histogram Equalization'
        },
        {
            'id': 'morphological',
            'name': 'Morphological Operations',
            'description': 'Closing and opening operations'
        },
        {
            'id': 'denoise',
            'name': 'Denoising',
            'description': 'Non-local means denoising'
        }
    ]
    return jsonify(methods)


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get supported OCR languages."""
    # Common Tesseract languages
    languages = [
        {'code': 'eng', 'name': 'English'},
        {'code': 'fra', 'name': 'French'},
        {'code': 'deu', 'name': 'German'},
        {'code': 'spa', 'name': 'Spanish'},
        {'code': 'ita', 'name': 'Italian'},
        {'code': 'por', 'name': 'Portuguese'},
        {'code': 'rus', 'name': 'Russian'},
        {'code': 'jpn', 'name': 'Japanese'},
        {'code': 'hin', 'name': 'Hindi'},
        {'code': 'ara', 'name': 'Arabic'},
        {'code': 'chi_sim', 'name': 'Chinese (Simplified)'},
        {'code': 'chi_tra', 'name': 'Chinese (Traditional)'},
    ]
    return jsonify(languages)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'Document Scanner API is running'})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {error}")
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Document Scanner Web Server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
