# How to Run Document Scanner & OCR - Complete Guide

## 📋 Table of Contents
1. [First-Time Setup](#first-time-setup)
2. [Running the Application](#running-the-application)
3. [Different Usage Scenarios](#different-usage-scenarios)
4. [Troubleshooting](#troubleshooting)

---

## 🔧 First-Time Setup

### Prerequisites Installation

#### Step 1: Install Python 3.7+

**Windows:**
- Download from: https://www.python.org/downloads/
- Run the installer
- ✅ **IMPORTANT**: Check "Add Python to PATH"
- Click "Install Now"

**Verify installation:**
```powershell
python --version
pip --version
```

#### Step 2: Install Tesseract-OCR (REQUIRED)

**Windows:**

1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
   - Look for: `tesseract-ocr-w64-setup-v5.x.x.exe`

2. Run installer with these settings:
   - Installation folder: `C:\Program Files\Tesseract-OCR` (default)
   - Languages: Select languages you need (minimum: English)
   - ✅ All other settings can be default

3. Verify installation:
   ```powershell
   "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   ```

### Step 3: Setup Project

#### Option A: Automatic Setup (Easiest)

**Windows:**
```powershell
cd c:\Users\91743\Lucifer\document-scanner-ocr
run.bat
```

This will:
- Create virtual environment ✓
- Install all dependencies ✓
- Check setup ✓
- Offer menu to start using ✓

#### Option B: Manual Setup

**Windows:**
```powershell
# 1. Navigate to project folder
cd c:\Users\91743\Lucifer\document-scanner-ocr

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify setup
python quickstart.py
```

**Detailed explanation:**
- Virtual environment: Isolated Python environment for this project
- Dependencies: Required Python packages (OpenCV, PyTesseract, etc.)
- Quickstart: Checks if everything is installed correctly

---

## 🚀 Running the Application

### Method 1: Web Interface (Recommended for Beginners)

**Start the server:**
```powershell
# Make sure virtual environment is activated
venv\Scripts\activate

# Start web server
python web_app.py
```

**Expected output:**
```
Starting Document Scanner Web Server...
Open http://localhost:5000 in your browser
 * Running on http://0.0.0.0:5000
```

**How to use:**
1. Open browser: http://localhost:5000
2. Click to upload or drag-drop a document image
3. Select preprocessing method (default: "Adaptive Thresholding")
4. Select OCR language (default: English)
5. Click "Scan Document" button
6. Wait for results (usually 1-3 seconds)
7. View processed images and extracted text
8. Download or copy extracted text

**Stop the server:** Press `Ctrl + C` in terminal

### Method 2: Command-Line Interface (CLI)

**For single document:**
```powershell
# Activate environment
venv\Scripts\activate

# Scan document
python cli.py single document.jpg

# Save result to file
python cli.py single document.jpg -o result.txt

# Specify preprocessing method
python cli.py single document.jpg -p clahe

# Different language
python cli.py single document_french.jpg -l fra
```

**For batch processing:**
```powershell
# Scan all documents in folder
python cli.py batch ./documents

# Save results
python cli.py batch ./documents -o ./results

# Different method and language
python cli.py batch ./documents -p morphological -l eng -o ./results
```

**Compare preprocessing methods:**
```powershell
# Find best method for your document
python cli.py compare document.jpg
```

**Available preprocessing methods:**
```
adaptive      - Best for varying lighting (default)
otsu          - Automatic thresholding
clahe         - Contrast enhancement
morphological - Noise reduction
denoise       - Non-local means denoising
```

**Available languages:**
```
eng - English       fra - French        deu - German
spa - Spanish       ita - Italian       por - Portuguese
rus - Russian       jpn - Japanese      hin - Hindi
ara - Arabic        chi_sim/chi_tra - Chinese
```

### Method 3: Run Python Examples

**Execute all examples:**
```powershell
venv\Scripts\activate
python examples.py
```

**This will:**
1. ✓ Create sample documents
2. ✓ Demonstrate single scanning
3. ✓ Compare preprocessing methods
4. ✓ Show batch processing
5. ✓ Save results to `output/` folder

**View results:**
```powershell
# Open output folder
start output\
```

### Method 4: Use as Python Library

**In your own Python script:**
```python
from document_scanner import DocumentScanner

# Initialize
scanner = DocumentScanner()

# Scan document
result = scanner.scan_document('document.jpg')

# Access results
if result['success']:
    print(result['text'])
    
# Save processed images
scanner.save_processed_images('processed')
```

### Method 5: Quick Start with Minimal Commands

**Absolute quickest way (after setup):**
```powershell
# Terminal 1: Start web server
cd c:\Users\91743\Lucifer\document-scanner-ocr
venv\Scripts\activate
python web_app.py

# Terminal 2: Open browser
start http://localhost:5000
```

---

## 📚 Different Usage Scenarios

### Scenario 1: Scan One Document (User)

**Goal:** Quickly scan a single document and get text

```powershell
# Terminal steps:
cd c:\Users\91743\Lucifer\document-scanner-ocr
venv\Scripts\activate

# Place your document.jpg in the project folder

# Scan it
python cli.py single document.jpg

# View output
type result.txt
```

**Result:** Text printed to console + saved in `output/`

### Scenario 2: Batch Process All Documents (User)

**Goal:** Scan 50 documents automatically

```powershell
venv\Scripts\activate

# Put all PDFs /images in 'documents' folder
# Scan all
python cli.py batch documents -o results

# Results in results/ folder, one file per document
```

### Scenario 3: Find Best Settings (User)

**Goal:** Determine optimal preprocessing for your documents

```powershell
venv\Scripts\activate

# Test all 5 methods
python cli.py compare problem_document.jpg

# Output shows which method worked best
```

### Scenario 4: Web Interface for Team (Admin)

**Goal:** Share scanning tool with team members

**Setup once:**
```powershell
# Install and setup
cd c:\Users\91743\Lucifer\document-scanner-ocr
venv\Scripts\activate
pip install -r requirements.txt
```

**Daily use:**
```powershell
# Start server
cd c:\Users\91743\Lucifer\document-scanner-ocr
venv\Scripts\activate
python web_app.py
```

**Team uses:**
- Open http://your-computer-ip:5000 in browser
- Upload documents
- Get results immediately

### Scenario 5: Integrated Into Another Application

**In your Python code:**
```python
from document_scanner import DocumentScanner
import os

def extract_text_from_document(file_path):
    scanner = DocumentScanner()
    result = scanner.scan_document(file_path, preprocessing_method='adaptive')
    return result['text'] if result['success'] else None

# Use it
text = extract_text_from_document('invoice.jpg')
print(text)
```

---

## 🆘 Troubleshooting

### Issue 1: "Python not found"

**Error:** `'python' is not recognized as an internal or external command`

**Solution:**
```powershell
# Option 1: Use full path
C:\Users\YourUsername\AppData\Local\Programs\Python\Python39\python.exe --version

# Option 2: Reinstall Python with PATH option
# Download Python from python.org, run installer,
# Check "Add Python to PATH", click Install Now

# Option 3: Verify Python location
where python
```

### Issue 2: "Tesseract is not installed"

**Error:** `TesseractNotFoundError: tesseract is not installed`

**Solution:**
```powershell
# 1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
# 2. Install to: C:\Program Files\Tesseract-OCR
# 3. Verify:
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version

# 4. If different location, edit scanner.py:
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\your\path\tesseract.exe'
```

### Issue 3: "Could not detect document edges"

**Problem:** Script says "Could not detect document edges"

**Solution:**
```powershell
# 1. Try different preprocessing method
python cli.py compare document.jpg

# 2. Or use web interface to test methods
python web_app.py
# Test different preprocessing options

# 3. Try:
#    - Better document image (clearer edges)
#    - Better lighting
#    - Different angle
```

### Issue 4: "Out of memory" or slow processing

**Problem:** Application becomes slow or crashes with large images

**Solution:**
```python
# Resize image before scanning
import cv2
from document_scanner import DocumentScanner

img = cv2.imread('large_image.jpg')
small_img = cv2.resize(img, (1024, 768))
cv2.imwrite('resized.jpg', small_img)

# Then scan
scanner = DocumentScanner()
result = scanner.scan_document('resized.jpg')
```

### Issue 5: "Web interface won't open"

**Error:** Cannot connect to http://localhost:5000

**Solution:**
```powershell
# 1. Check if server started
# Look for "Running on http://0.0.0.0:5000" message

# 2. Try different port
# Edit web_app.py, last line:
# app.run(debug=True, host='0.0.0.0', port=8000)

# 3. Check firewall
# Windows Firewall may block it
# Add Python to firewall exceptions

# 4. Use IP address instead
# Open: http://127.0.0.1:5000
```

### Issue 6: "Permission denied" errors

**Error:** `PermissionError` when saving files

**Solution:**
```powershell
# 1. Run terminal as Administrator
# Right-click PowerShell → Run as Administrator

# 2. Check folder permissions
# Folder should be writable

# 3. Change output folder
# In code, use temp folder:
scanner.save_processed_images(r'C:\Temp\output')
```

### Issue 7: "OCR accuracy is poor"

**Problem:** Extracted text has many errors

**Solution:**
```powershell
# 1. Try different preprocessing
python cli.py compare document.jpg

# 2. Use CLAHE for low contrast
python cli.py single document.jpg -p clahe

# 3. Use better image
#    - Higher resolution
#    - Better lighting
#    - Straight document (not skewed)
```

### Issue 8: "Module not found"

**Error:** `ModuleNotFoundError: No module named 'cv2'`

**Solution:**
```powershell
# 1. Make sure virtual environment is activated
venv\Scripts\activate

# 2. Reinstall requirements
pip install -r requirements.txt

# 3. Verify installation
python -c "import cv2; print(cv2.__version__)"
```

---

## ✅ Verification Checklist

After setup, verify everything works:

```powershell
# 1. Python installed
python --version
# Expected: Python 3.7+

# 2. Tesseract installed
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version
# Expected: tesseract 5.x.x

# 3. Dependencies installed
venv\Scripts\activate
python -c "import cv2, pytesseract, imutils, flask; print('All imported!')"
# Expected: All imported!

# 4. Document Scanner works
python quickstart.py
# Expected: ✓ ALL CHECKS PASSED

# 5. Run test
python examples.py
# Expected: Examples complete successfully
```

---

## 🚀 Quick Reference Commands

### Setup (First time only)
```powershell
cd c:\Users\91743\Lucifer\document-scanner-ocr
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Activate Environment (Every session)
```powershell
venv\Scripts\activate
```

### Single Scan
```powershell
python cli.py single document.jpg
```

### Web Interface
```powershell
python web_app.py
# Open: http://localhost:5000
```

### Batch Processing
```powershell
python cli.py batch ./documents -o ./results
```

### Run Examples
```powershell
python examples.py
```

### Check Setup
```powershell
python quickstart.py
```

---

## 📞 Need Help?

1. **Check README.md** - Comprehensive documentation
2. **Run quickstart.py** - Verify installation
3. **Run examples.py** - See working examples
4. **Read this file** - Current guide

---

**Version:** 1.0  
**Last Updated:** April 15, 2026  
**Status:** Complete ✓
