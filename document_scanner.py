"""
Advanced Document Scanner with OCR Enhancement
Complete system for automatic document detection, perspective transformation,
and high-accuracy text extraction using Tesseract OCR.
"""

import cv2
import numpy as np
import pytesseract
import imutils
from pathlib import Path
from typing import Tuple, Optional, Dict, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentScanner:
    """Advanced document scanner with multiple preprocessing techniques."""

    def __init__(self, tesseract_path: Optional[str] = None, debug: bool = False):
        """
        Initialize the document scanner.
        
        Args:
            tesseract_path: Path to Tesseract executable
            debug: Enable debug mode for visualizations
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        self.debug = debug
        self.original_image = None
        self.processed_image = None
        self.warped_image = None
        
    def load_image(self, image_path: str) -> bool:
        """
        Load an image from file.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.original_image = cv2.imread(image_path)
            if self.original_image is None:
                logger.error(f"Error: Could not load image from {image_path}")
                return False
            logger.info(f"Successfully loaded image: {image_path}")
            return True
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            return False

    def from_array(self, image_array: np.ndarray) -> None:
        """
        Load image from numpy array.
        
        Args:
            image_array: Numpy array representing the image
        """
        self.original_image = image_array.copy()
        logger.info("Image loaded from array")

    def detect_document_boundaries(self, image: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Detect document boundaries using edge and contour detection.
        
        Args:
            image: Input image (if None, uses original)
            
        Returns:
            Processed image and contour points
        """
        if image is None:
            image = self.original_image.copy()
        
        if image is None:
            logger.error("No image loaded")
            return image, None
        
        # Resize for faster processing
        ratio = image.shape[0] / 500.0
        original = image.copy()
        image = imutils.resize(image, height=500)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection with optimal parameters
        edges = cv2.Canny(blurred, 75, 200)
        
        if self.debug:
            cv2.imshow("Edges", edges)
        
        # Find contours
        contours = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        
        document_contour = None
        
        # Find the contour with 4 points (document)
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            if len(approx) == 4:
                document_contour = approx * ratio
                break
        
        if document_contour is None:
            logger.warning("Could not detect document edges, attempting fallback")
            document_contour = np.array([
                [0, 0],
                [original.shape[1], 0],
                [original.shape[1], original.shape[0]],
                [0, original.shape[0]]
            ], dtype=np.float32)
        
        return original, document_contour

    @staticmethod
    def four_point_transform(image: np.ndarray, pts: np.ndarray) -> np.ndarray:
        """
        Perform a four-point perspective transform.
        
        Args:
            image: Input image
            pts: Four corner points
            
        Returns:
            Transformed image
        """
        pts = pts.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        
        # Top-left: smallest sum, Bottom-right: largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # Top-right: smallest diff, Bottom-left: largest diff
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        (tl, tr, br, bl) = rect
        
        # Calculate width
        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = max(int(widthA), int(widthB))
        
        # Calculate height
        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = max(int(heightA), int(heightB))
        
        # Destination points
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]
        ], dtype="float32")
        
        # Perspective transformation matrix
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        
        return warped

    def apply_perspective_transform(self, image: Optional[np.ndarray] = None, 
                                   contour: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Apply perspective transformation to the image.
        
        Args:
            image: Input image
            contour: Document contour points
            
        Returns:
            Transformed image
        """
        if image is None:
            image = self.original_image
        
        if contour is None:
            _, contour = self.detect_document_boundaries(image)
        
        if contour is None:
            logger.warning("Could not apply perspective transform")
            return image
        
        warped = self.four_point_transform(image, contour)
        self.warped_image = warped.copy()
        logger.info(f"Perspective transform applied. Shape: {warped.shape}")
        
        return warped

    @staticmethod
    def enhance_image_adaptive(image: np.ndarray) -> np.ndarray:
        """
        Enhance image using adaptive thresholding.
        
        Args:
            image: Input image
            
        Returns:
            Enhanced image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        enhanced = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        return enhanced

    @staticmethod
    def enhance_image_otsu(image: np.ndarray) -> np.ndarray:
        """
        Enhance image using Otsu's thresholding.
        
        Args:
            image: Input image
            
        Returns:
            Enhanced image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        _, enhanced = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return enhanced

    @staticmethod
    def enhance_image_denoise(image: np.ndarray) -> np.ndarray:
        """
        Enhance image using denoising.
        
        Args:
            image: Input image
            
        Returns:
            Denoised image
        """
        if len(image.shape) == 3:
            denoised = cv2.fastNlMeansDenoisingColored(image, None, h=10, hForColorComponents=10, 
                                                       templateWindowSize=7, searchWindowSize=21)
        else:
            denoised = cv2.fastNlMeansDenoising(image, None, h=10, 
                                               templateWindowSize=7, searchWindowSize=21)
        return denoised

    @staticmethod
    def enhance_image_clahe(image: np.ndarray) -> np.ndarray:
        """
        Enhance image using CLAHE (Contrast Limited Adaptive Histogram Equalization).
        
        Args:
            image: Input image
            
        Returns:
            Enhanced image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        return enhanced

    @staticmethod
    def enhance_image_morphological(image: np.ndarray) -> np.ndarray:
        """
        Enhance image using morphological operations.
        
        Args:
            image: Input image
            
        Returns:
            Enhanced image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        enhanced = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        enhanced = cv2.morphologyEx(enhanced, cv2.MORPH_OPEN, kernel)
        return enhanced

    def preprocess_image(self, warped: Optional[np.ndarray] = None, 
                        method: str = "adaptive") -> np.ndarray:
        """
        Preprocess image for OCR with various enhancement techniques.
        
        Args:
            warped: Input warped image
            method: Preprocessing method ('adaptive', 'otsu', 'denoise', 'clahe', 'morphological')
            
        Returns:
            Preprocessed image
        """
        if warped is None:
            warped = self.warped_image
        
        if warped is None:
            logger.error("No warped image available")
            return None
        
        logger.info(f"Applying {method} preprocessing")
        
        methods = {
            'adaptive': self.enhance_image_adaptive,
            'otsu': self.enhance_image_otsu,
            'denoise': self.enhance_image_denoise,
            'clahe': self.enhance_image_clahe,
            'morphological': self.enhance_image_morphological
        }
        
        if method not in methods:
            logger.warning(f"Unknown preprocessing method: {method}. Using adaptive.")
            method = 'adaptive'
        
        processed = methods[method](warped)
        self.processed_image = processed.copy()
        
        return processed

    def extract_text(self, image: Optional[np.ndarray] = None, 
                    lang: str = "eng", psm: int = 3) -> str:
        """
        Extract text from image using Tesseract OCR.
        
        Args:
            image: Input image (if None, uses processed image)
            lang: Language for OCR
            psm: Tesseract PSM (Page Segmentation Mode)
                1: Automatic page segmentation with OSD
                3: Fully automatic page segmentation (default)
                6: Uniform block of text
                
        Returns:
            Extracted text
        """
        if image is None:
            image = self.processed_image
        
        if image is None:
            logger.error("No image available for OCR")
            return ""
        
        try:
            logger.info(f"Extracting text using Tesseract (lang={lang}, psm={psm})")
            config = f'--psm {psm}'
            text = pytesseract.image_to_string(image, lang=lang, config=config)
            logger.info(f"Extracted {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error during OCR: {e}")
            return ""

    def scan_document(self, image_path: str, preprocessing_method: str = "adaptive", 
                     lang: str = "eng") -> Dict:
        """
        Complete document scanning pipeline.
        
        Args:
            image_path: Path to the document image
            preprocessing_method: Method for image enhancement
            lang: Language for OCR
            
        Returns:
            Dictionary with results
        """
        logger.info("Starting document scan...")
        
        # Load image
        if not self.load_image(image_path):
            return {"success": False, "error": "Failed to load image"}
        
        # Detect document boundaries
        original, contour = self.detect_document_boundaries()
        
        # Apply perspective transform
        warped = self.apply_perspective_transform(original, contour)
        
        # Preprocess image
        processed = self.preprocess_image(warped, method=preprocessing_method)
        
        # Extract text
        text = self.extract_text(processed, lang=lang)
        
        logger.info("Document scan completed successfully")
        
        return {
            "success": True,
            "text": text,
            "original_shape": original.shape,
            "processed_shape": processed.shape,
            "preprocessing_method": preprocessing_method
        }

    def save_processed_images(self, output_dir: str) -> None:
        """
        Save processed images for inspection.
        
        Args:
            output_dir: Directory to save images
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        if self.original_image is not None:
            cv2.imwrite(f"{output_dir}/1_original.jpg", self.original_image)
        
        if self.warped_image is not None:
            cv2.imwrite(f"{output_dir}/2_warped.jpg", self.warped_image)
        
        if self.processed_image is not None:
            cv2.imwrite(f"{output_dir}/3_processed.jpg", self.processed_image)
        
        logger.info(f"Processed images saved to {output_dir}")

    def batch_scan_documents(self, image_folder: str, preprocessing_method: str = "adaptive", 
                            lang: str = "eng") -> List[Dict]:
        """
        Scan multiple documents in a folder.
        
        Args:
            image_folder: Folder containing images
            preprocessing_method: Method for image enhancement
            lang: Language for OCR
            
        Returns:
            List of results for each document
        """
        results = []
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        image_folder_path = Path(image_folder)
        
        if not image_folder_path.exists():
            logger.error(f"Folder not found: {image_folder}")
            return results
        
        images = [f for f in image_folder_path.iterdir() 
                 if f.suffix.lower() in image_extensions]
        
        logger.info(f"Found {len(images)} images to process")
        
        for idx, image_path in enumerate(images, 1):
            logger.info(f"Processing [{idx}/{len(images)}] {image_path.name}")
            result = self.scan_document(str(image_path), preprocessing_method, lang)
            result['filename'] = image_path.name
            results.append(result)
        
        return results


if __name__ == "__main__":
    print("Document Scanner Module - Import this to use the DocumentScanner class")
