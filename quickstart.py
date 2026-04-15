"""
Quick Start Guide - 5 Minute Setup
Fast track to get Document Scanner & OCR working
"""

import sys
from pathlib import Path

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 3.7+ required. You have: {version.major}.{version.minor}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if all dependencies are installed."""
    dependencies = {
        'cv2': 'OpenCV',
        'pytesseract': 'PyTesseract',
        'imutils': 'Imutils',
        'numpy': 'NumPy',
        'flask': 'Flask (optional, for web interface)'
    }
    
    print("\nChecking dependencies:")
    all_installed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_tesseract():
    """Check Tesseract installation."""
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"\n✓ Tesseract found: {version}")
        return True
    except Exception as e:
        print(f"\n❌ Tesseract not found: {e}")
        print("   Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def main():
    """Run quick start checks and provide guidance."""
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  📄 DOCUMENT SCANNER & OCR - QUICK START".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    print("\n🔍 Checking setup...\n")
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Please upgrade Python to 3.7 or higher")
        return 1
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Check Tesseract
    if not check_tesseract():
        print("\n⚠️  Install Tesseract-OCR from:")
        print("   https://github.com/UB-Mannheim/tesseract/wiki")
        return 1
    
    # All checks passed
    print("\n" + "="*68)
    print("✓ ALL CHECKS PASSED - READY TO USE!")
    print("="*68)
    
    print("\n🚀 Quick Start Options:\n")
    
    print("1️⃣  WEB INTERFACE (Recommended for beginners):")
    print("   python web_app.py")
    print("   Then open: http://localhost:5000\n")
    
    print("2️⃣  COMMAND LINE (Single document):")
    print("   python cli.py single document.jpg\n")
    
    print("3️⃣  BATCH PROCESSING (Multiple documents):")
    print("   python cli.py batch ./documents\n")
    
    print("4️⃣  RUN EXAMPLES (Test all features):")
    print("   python examples.py\n")
    
    print("5️⃣  COMPARE METHODS (Find best preprocessing):")
    print("   python cli.py compare document.jpg\n")
    
    print("📖 For detailed help:")
    print("   - Read README.md for complete documentation")
    print("   - Run: python cli.py --help")
    print("   - Run: python cli.py single --help\n")
    
    print("💡 Next Steps:")
    print("   1. Place your document image in the project folder")
    print("   2. Choose an option above and run the command")
    print("   3. Check the 'output' folder for results\n")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
