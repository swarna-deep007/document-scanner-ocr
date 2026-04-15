"""
Command-Line Interface for Document Scanner & OCR
Easy-to-use CLI tool for batch processing and single document scanning.
"""

import argparse
import sys
from pathlib import Path
from document_scanner import DocumentScanner
import logging
from tabulate import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def scan_single(args):
    """Handle single document scanning."""
    print("\n" + "="*70)
    print("SINGLE DOCUMENT SCANNER")
    print("="*70 + "\n")
    
    # Validate file exists
    if not Path(args.input).exists():
        print(f"❌ Error: File not found - {args.input}")
        return 1
    
    # Initialize scanner
    scanner = DocumentScanner(
        tesseract_path=args.tesseract,
        debug=args.debug
    )
    
    # Scan document
    print(f"📄 Scanning: {args.input}")
    print(f"📋 Method: {args.preprocessing}")
    print(f"🌐 Language: {args.language}\n")
    
    result = scanner.scan_document(
        args.input,
        preprocessing_method=args.preprocessing,
        lang=args.language
    )
    
    if not result['success']:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return 1
    
    # Display results
    print("\n" + "-"*70)
    print("✓ SCAN SUCCESSFUL")
    print("-"*70)
    print(f"Original shape: {result['original_shape']}")
    print(f"Processed shape: {result['processed_shape']}")
    print(f"Characters extracted: {len(result['text'])}\n")
    
    # Save processed images if requested
    if args.output_images:
        output_dir = args.output_images
        scanner.save_processed_images(output_dir)
        print(f"💾 Processed images saved to: {output_dir}\n")
    
    # Display extracted text
    print("-"*70)
    print("📄 EXTRACTED TEXT")
    print("-"*70)
    print(result['text'])
    print("-"*70 + "\n")
    
    # Save text if requested
    if args.output_text:
        with open(args.output_text, 'w', encoding='utf-8') as f:
            f.write(result['text'])
        print(f"💾 Text saved to: {args.output_text}\n")
    
    return 0


def scan_batch(args):
    """Handle batch document scanning."""
    print("\n" + "="*70)
    print("BATCH DOCUMENT SCANNER")
    print("="*70 + "\n")
    
    # Validate directory exists
    if not Path(args.input_dir).exists():
        print(f"❌ Error: Directory not found - {args.input_dir}")
        return 1
    
    # Initialize scanner
    scanner = DocumentScanner(
        tesseract_path=args.tesseract,
        debug=args.debug
    )
    
    # Scan batch
    print(f"📁 Input directory: {args.input_dir}")
    print(f"📋 Method: {args.preprocessing}")
    print(f"🌐 Language: {args.language}\n")
    
    results = scanner.batch_scan_documents(
        args.input_dir,
        preprocessing_method=args.preprocessing,
        lang=args.language
    )
    
    if not results:
        print("❌ No documents found or processed")
        return 1
    
    # Display summary
    print("\n" + "-"*70)
    print("✓ BATCH PROCESSING COMPLETED")
    print("-"*70 + "\n")
    
    # Create summary table
    table_data = []
    successful = 0
    total_chars = 0
    
    for result in results:
        if result['success']:
            successful += 1
            total_chars += len(result['text'])
            status = "✓ Success"
        else:
            status = "✗ Failed"
        
        table_data.append([
            result['filename'],
            status,
            len(result['text']) if result['success'] else 0
        ])
    
    print(tabulate(table_data, headers=['Filename', 'Status', 'Characters'], tablefmt='grid'))
    
    print(f"\nTotal: {len(results)} files")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")
    print(f"Total characters: {total_chars}\n")
    
    # Save output if requested
    if args.output_dir:
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
        
        for idx, result in enumerate(results, 1):
            if result['success']:
                filename = Path(result['filename']).stem
                output_file = Path(args.output_dir) / f"{filename}_extracted.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result['text'])
        
        print(f"💾 Results saved to: {args.output_dir}\n")
    
    return 0


def compare_methods(args):
    """Compare different preprocessing methods."""
    print("\n" + "="*70)
    print("PREPROCESSING METHOD COMPARISON")
    print("="*70 + "\n")
    
    # Validate file exists
    if not Path(args.input).exists():
        print(f"❌ Error: File not found - {args.input}")
        return 1
    
    # Initialize scanner
    scanner = DocumentScanner(
        tesseract_path=args.tesseract,
        debug=False
    )
    
    # Compare methods
    methods = ['adaptive', 'otsu', 'clahe', 'morphological', 'denoise']
    results = {}
    
    print(f"📄 Input: {args.input}")
    print(f"🌐 Language: {args.language}\n")
    print("Processing with different methods...\n")
    
    for method in methods:
        print(f"  Processing with: {method:<15}", end=" ")
        result = scanner.scan_document(
            args.input,
            preprocessing_method=method,
            lang=args.language
        )
        
        if result['success']:
            char_count = len(result['text'])
            results[method] = {
                'characters': char_count,
                'text': result['text']
            }
            print(f"✓ ({char_count} characters)")
        else:
            print("✗ Failed")
    
    # Display comparison
    print("\n" + "-"*70)
    print("COMPARISON RESULTS")
    print("-"*70 + "\n")
    
    table_data = []
    for method, data in sorted(results.items(), key=lambda x: x[1]['characters'], reverse=True):
        text_preview = data['text'][:50].replace('\n', ' ')
        table_data.append([method, data['characters'], text_preview + "..."])
    
    print(tabulate(table_data, headers=['Method', 'Characters', 'Preview'], tablefmt='grid'))
    print("\n")
    
    # Recommend best method
    if results:
        best_method = max(results.items(), key=lambda x: x[1]['characters'])[0]
        print(f"💡 Recommended method: {best_method}")
        print("   (Extracted the most text)\n")
    
    return 0


def show_info(args):
    """Show system information."""
    print("\n" + "="*70)
    print("SYSTEM INFORMATION")
    print("="*70 + "\n")
    
    try:
        import cv2
        print(f"OpenCV version: {cv2.__version__}")
    except:
        print("OpenCV: Not installed")
    
    try:
        import pytesseract
        print(f"PyTesseract: Installed")
        try:
            result = pytesseract.get_tesseract_version()
            print(f"Tesseract version: {result}")
        except:
            print("Tesseract: Not found (install Tesseract-OCR)")
    except:
        print("PyTesseract: Not installed")
    
    try:
        import imutils
        print(f"Imutils: Installed")
    except:
        print("Imutils: Not installed")
    
    print("\n")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Document Scanner & OCR - Advanced document digitization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a single document
  python cli.py single document.jpg

  # Scan with specific preprocessing method
  python cli.py single document.jpg -p clahe -o result.txt

  # Batch process documents
  python cli.py batch ./documents -o ./results

  # Compare preprocessing methods
  python cli.py compare document.jpg

  # Show system information
  python cli.py info
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Single scan command
    single_parser = subparsers.add_parser('single', help='Scan a single document')
    single_parser.add_argument('input', help='Input image file')
    single_parser.add_argument('-p', '--preprocessing', 
                              choices=['adaptive', 'otsu', 'clahe', 'morphological', 'denoise'],
                              default='adaptive',
                              help='Preprocessing method (default: adaptive)')
    single_parser.add_argument('-l', '--language', 
                              default='eng',
                              help='OCR language (default: eng)')
    single_parser.add_argument('-o', '--output-text',
                              help='Save extracted text to file')
    single_parser.add_argument('-i', '--output-images',
                              help='Save processed images to directory')
    single_parser.add_argument('-t', '--tesseract',
                              help='Path to Tesseract executable')
    single_parser.add_argument('--debug', action='store_true',
                              help='Enable debug mode')
    single_parser.set_defaults(func=scan_single)
    
    # Batch scan command
    batch_parser = subparsers.add_parser('batch', help='Scan documents in batch')
    batch_parser.add_argument('input_dir', help='Input directory containing images')
    batch_parser.add_argument('-p', '--preprocessing',
                             choices=['adaptive', 'otsu', 'clahe', 'morphological', 'denoise'],
                             default='adaptive',
                             help='Preprocessing method (default: adaptive)')
    batch_parser.add_argument('-l', '--language',
                             default='eng',
                             help='OCR language (default: eng)')
    batch_parser.add_argument('-o', '--output-dir',
                             help='Save results to directory')
    batch_parser.add_argument('-t', '--tesseract',
                             help='Path to Tesseract executable')
    batch_parser.add_argument('--debug', action='store_true',
                             help='Enable debug mode')
    batch_parser.set_defaults(func=scan_batch)
    
    # Compare methods command
    compare_parser = subparsers.add_parser('compare', help='Compare preprocessing methods')
    compare_parser.add_argument('input', help='Input image file')
    compare_parser.add_argument('-l', '--language',
                               default='eng',
                               help='OCR language (default: eng)')
    compare_parser.add_argument('-t', '--tesseract',
                               help='Path to Tesseract executable')
    compare_parser.set_defaults(func=compare_methods)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show system information')
    info_parser.set_defaults(func=show_info)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Execute command
    try:
        return args.func(args)
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
