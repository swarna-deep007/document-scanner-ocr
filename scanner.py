"""
Document Scanner & OCR - Original Simple Script
Basic implementation for quick document scanning

For a full-featured application, see:
- document_scanner.py: Main class with advanced features
- cli.py: Command-line interface
- web_app.py: Web interface
- examples.py: Usage examples

This script provides a quick way to scan documents.
"""

from document_scanner import DocumentScanner
from pathlib import Path

def main():
    """
    Simple document scanning example.
    Place your document image as 'document.jpg' in this folder.
    """
    
    image_file = "document.jpg"
    
    # Check if image exists
    if not Path(image_file).exists():
        print(f"❌ Error: {image_file} not found!")
        print("\nUsage:")
        print("  1. Place a document image as 'document.jpg'")
        print("  2. Run this script: python scanner.py")
        print("\nAlternatively, use:")
        print("  - python cli.py single your_image.jpg")
        print("  - python web_app.py  (then open http://localhost:5000)")
        return 1
    
    print("📄 Document Scanner & OCR")
    print("="*50)
    print(f"Scanning: {image_file}\n")
    
    # Create scanner instance
    scanner = DocumentScanner()
    
    # Scan document with default settings
    print("⏳ Processing document...")
    result = scanner.scan_document(
        image_file,
        preprocessing_method='adaptive',  # Best for most documents
        lang='eng'  # English language
    )
    
    # Display results
    if result['success']:
        print("\n✓ Scan completed successfully!")
        print(f"  Original size: {result['original_shape']}")
        print(f"  Processed size: {result['processed_shape']}")
        print(f"  Text extracted: {len(result['text'])} characters\n")
        
        print("="*50)
        print("📄 EXTRACTED TEXT")
        print("="*50)
        print(result['text'])
        print("="*50 + "\n")
        
        # Save results
        print("💾 Saving processed images to 'output' folder...")
        scanner.save_processed_images('output')
        print("✓ Done!\n")
        
        # Save text
        with open('extracted_text.txt', 'w', encoding='utf-8') as f:
            f.write(result['text'])
        print("✓ Text saved to: extracted_text.txt\n")
        
        # Display image processing pipeline
        print("📊 Processing Pipeline:")
        print("  1. output/1_original.jpg   - Original document")
        print("  2. output/2_warped.jpg     - Perspective corrected")
        print("  3. output/3_processed.jpg  - Enhanced for OCR\n")
        
        return 0
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}\n")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())