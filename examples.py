"""
Example usage of the Document Scanner with various preprocessing techniques.
Demonstrates the complete scanning pipeline with different scenarios.
"""

import cv2
import numpy as np
from document_scanner import DocumentScanner
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_single_document_scan():
    """Example: Scan a single document with adaptive thresholding."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Single Document Scan")
    print("="*60)
    
    # Initialize scanner
    scanner = DocumentScanner(debug=False)
    
    # Try to scan document.jpg (create a sample if it doesn't exist)
    image_path = "document.jpg"
    
    if not Path(image_path).exists():
        print(f"⚠️  {image_path} not found. Creating a sample image...")
        create_sample_document()
    
    # Scan document
    result = scanner.scan_document(
        image_path,
        preprocessing_method="adaptive",
        lang="eng"
    )
    
    if result['success']:
        print("\n✓ Scan successful!")
        print(f"Original shape: {result['original_shape']}")
        print(f"Processed shape: {result['processed_shape']}")
        print(f"Preprocessing method: {result['preprocessing_method']}")
        print("\n--- Extracted Text ---")
        print(result['text'][:500])  # Print first 500 characters
        
        # Save processed images
        scanner.save_processed_images("output/example1")
    else:
        print(f"✗ Scan failed: {result.get('error', 'Unknown error')}")


def example_multiple_preprocessing_methods():
    """Example: Compare different preprocessing methods."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Multiple Preprocessing Methods Comparison")
    print("="*60)
    
    image_path = "document.jpg"
    
    if not Path(image_path).exists():
        print(f"⚠️  {image_path} not found. Creating a sample image...")
        create_sample_document()
    
    methods = ["adaptive", "otsu", "clahe", "morphological"]
    results = {}
    
    scanner = DocumentScanner(debug=False)
    
    for method in methods:
        print(f"\nTesting method: {method}")
        result = scanner.scan_document(
            image_path,
            preprocessing_method=method,
            lang="eng"
        )
        
        if result['success']:
            text_preview = result['text'][:200].replace('\n', ' ')
            print(f"✓ Method '{method}' - Characters extracted: {len(result['text'])}")
            print(f"  Preview: {text_preview}...")
            results[method] = result
        else:
            print(f"✗ Method '{method}' failed")
    
    print("\n" + "-"*60)
    print("Summary:")
    for method, result in results.items():
        print(f"  {method}: {len(result['text'])} characters")


def example_batch_processing():
    """Example: Process multiple documents in batch."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Batch Processing Documents")
    print("="*60)
    
    # Create sample documents folder
    batch_folder = "documents_batch"
    Path(batch_folder).mkdir(exist_ok=True)
    
    # Create multiple sample documents
    num_samples = 3
    print(f"Creating {num_samples} sample documents...")
    for i in range(num_samples):
        create_sample_document(f"{batch_folder}/document_{i+1}.jpg")
    
    # Process batch
    scanner = DocumentScanner(debug=False)
    results = scanner.batch_scan_documents(
        batch_folder,
        preprocessing_method="adaptive"
    )
    
    print(f"\nProcessed {len(results)} documents:")
    for idx, result in enumerate(results, 1):
        if result['success']:
            print(f"  {idx}. {result['filename']}: {len(result['text'])} characters")
        else:
            print(f"  {idx}. {result['filename']}: FAILED")


def example_real_time_camera():
    """Example: Real-time document scanning from webcam."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Real-Time Camera Scanning")
    print("="*60)
    print("Instructions:")
    print("  1. Show document to camera")
    print("  2. Press 's' to scan")
    print("  3. Press 'q' to quit")
    print("="*60 + "\n")
    
    scanner = DocumentScanner(debug=True)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("✗ Could not open camera")
        return
    
    captured_frame = None
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("✗ Failed to read from camera")
            break
        
        # Resize for display
        display_frame = cv2.resize(frame, (800, 600))
        cv2.putText(display_frame, "Press 's' to capture, 'q' to quit", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Camera Feed - Press 's' to Scan or 'q' to Quit", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s'):
            captured_frame = frame.copy()
            print("✓ Frame captured! Processing...")
            break
        elif key == ord('q'):
            print("Exiting camera mode...")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if captured_frame is not None:
        # Save and process
        temp_path = "temp_camera_frame.jpg"
        cv2.imwrite(temp_path, captured_frame)
        
        result = scanner.scan_document(
            temp_path,
            preprocessing_method="adaptive"
        )
        
        if result['success']:
            print("\n✓ Scan successful!")
            print("--- Extracted Text ---")
            print(result['text'])
        else:
            print("✗ Scan failed")
        
        # Cleanup
        Path(temp_path).unlink()


def create_sample_document(output_path: str = "document.jpg"):
    """Create a sample document image for testing."""
    # Create a document-like image with text
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # Add some text-like patterns and rectangles
    cv2.rectangle(img, (50, 50), (750, 550), (0, 0, 0), 2)
    cv2.putText(img, "SAMPLE DOCUMENT", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(img, "This is a test document for OCR.", (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img, "Lorem ipsum dolor sit amet, consectetur", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)
    cv2.putText(img, "adipiscing elit, sed do eiusmod tempor.", (100, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)
    cv2.putText(img, "Date: 2026-04-15", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    cv2.putText(img, "Signature: _________________", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)
    
    # Add some noise to make it more realistic
    noise = np.random.normal(0, 5, img.shape).astype(np.uint8)
    img = cv2.add(img, noise)
    
    # Slightly rotate and skew
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 2, 1)
    img = cv2.warpAffine(img, M, (cols, rows))
    
    cv2.imwrite(output_path, img)
    logger.info(f"Sample document created: {output_path}")


def main():
    """Run all examples."""
    print("\n" + "█"*60)
    print("█  DOCUMENT SCANNER & OCR - USAGE EXAMPLES")
    print("█"*60)
    
    try:
        # Create output directory
        Path("output").mkdir(exist_ok=True)
        
        # Run examples
        example_single_document_scan()
        example_multiple_preprocessing_methods()
        example_batch_processing()
        
        # Uncomment to test camera (requires webcam)
        # example_real_time_camera()
        
        print("\n" + "█"*60)
        print("█  ALL EXAMPLES COMPLETED")
        print("█"*60)
        print("\nCheck the 'output' folder for processed images.")
        
    except Exception as e:
        logger.error(f"Error in examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
