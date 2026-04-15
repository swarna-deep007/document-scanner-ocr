# 📂 Project Structure & File Guide

Complete directory structure and explanation of all files in the Document Scanner & OCR application.

```
document-scanner-ocr/
│
├── 📄 MAIN APPLICATION FILES
│   ├── document_scanner.py        ⭐ Core DocumentScanner class (main engine)
│   ├── cli.py                     ⭐ Command-line interface
│   ├── web_app.py                 ⭐ Flask web application
│   ├── scanner.py                 ⭐ Quick-start simple script
│   └── examples.py                ⭐ Usage examples and demonstrations
│
├── 🔧 CONFIGURATION & UTILITIES
│   ├── config.py                  Configuration settings
│   ├── quickstart.py              Setup verification script
│   └── requirements.txt           Python dependencies
│
├── 📚 DOCUMENTATION
│   ├── README.md                  Complete documentation
│   ├── HOW_TO_RUN.md              Detailed setup & running guide
│   ├── FILE_GUIDE.md              This file
│   └── ARCHITECTURE.md            (Optional) Technical architecture details
│
├── 🌐 WEB INTERFACE
│   ├── templates/
│   │   └── index.html             Web interface HTML
│   └── static/                    Static assets (future CSS/JS)
│
├── 📁 WORKING DIRECTORIES
│   ├── uploads/                   Uploaded files (web app)
│   ├── processed_images/          Processed images output (web app)
│   ├── output/                    Final results
│   ├── documents/                 For batch processing samples
│   ├── documents_batch/           Batch processing test folder
│   └── results/                   Batch processing results
│
├── 🪟 WINDOWS HELPERS
│   └── run.bat                    Quick-start batch script
│
└── 🐍 PYTHON VENV (created during setup)
    └── venv/                      Virtual environment (not shown here)
```

---

## 📄 File Descriptions

### ⭐ Core Application Files

#### `document_scanner.py` (Core Engine)
**Purpose:** Main DocumentScanner class with all scanning functionality
**Size:** ~700 lines
**Key Classes:**
- `DocumentScanner`: Main class for document scanning operations

**Key Methods:**
- `load_image()`: Load image from file
- `detect_document_boundaries()`: Find document edges
- `apply_perspective_transform()`: Correct skewed documents
- `preprocess_image()`: Enhance image (5 methods)
- `extract_text()`: Extract text with Tesseract
- `scan_document()`: Complete pipeline in one call
- `batch_scan_documents()`: Process multiple documents

**Usage:**
```python
from document_scanner import DocumentScanner
scanner = DocumentScanner()
result = scanner.scan_document('document.jpg')
```

---

#### `cli.py` (Command-Line Interface)
**Purpose:** Professional CLI tool for document scanning
**Size:** ~400 lines
**Features:**
- Single document scanning
- Batch processing
- Method comparison
- System information
- Multi-language support
- Progress tracking

**Commands:**
- `single`: Scan one document
- `batch`: Process folder
- `compare`: Test all preprocessing methods
- `info`: System information

**Usage:**
```bash
python cli.py single document.jpg
python cli.py batch ./documents -o ./results
python cli.py compare document.jpg
```

---

#### `web_app.py` (Flask Web Application)
**Purpose:** Web interface for document scanning
**Size:** ~300 lines
**Features:**
- Upload interface
- Real-time processing
- Multiple preprocessing methods
- Multi-language support
- Result visualization
- REST API endpoints

**API Endpoints:**
- `POST /api/scan`: Scan document
- `GET /api/preprocessing-methods`: List methods
- `GET /api/languages`: List languages
- `GET /api/health`: Health check

**Usage:**
```bash
python web_app.py
# Open http://localhost:5000
```

---

#### `scanner.py` (Quick-Start Script)
**Purpose:** Simple, ready-to-use document scanning script
**Size:** ~80 lines
**Features:**
- Minimal setup required
- Single document scanning
- Automatic result saving
- Clear output display

**Usage:**
```bash
# Place your document as 'document.jpg'
python scanner.py
```

**Output:**
- `output/` folder: Processed images
- `extracted_text.txt`: Extracted text
- Console: Text preview

---

#### `examples.py` (Examples & Demonstrations)
**Purpose:** Complete working examples of all features
**Size:** ~450 lines
**Examples:**
1. Single document scanning
2. Comparing preprocessing methods
3. Batch processing
4. Real-time camera scanning

**Usage:**
```bash
python examples.py
```

**Output:**
- Sample documents created
- Processing results in `output/`
- Console output with demonstrations

---

### 🔧 Configuration & Setup Files

#### `config.py` (Configuration Settings)
**Purpose:** Centralized configuration for all components
**Sections:**
- Tesseract paths and settings
- OCR parameters
- Image processing parameters
- Preprocessing settings
- File handling settings
- Web interface settings
- Performance tuning

**Usage:**
```python
from config import DEFAULT_PREPROCESSING
preprocessing_method = DEFAULT_PREPROCESSING
```

---

#### `quickstart.py` (Setup Verification)
**Purpose:** Verify all dependencies are installed
**Checks:**
- Python version
- Required packages
- Tesseract installation
- System readiness

**Usage:**
```bash
python quickstart.py
```

**Output:** ✓ All checks passed or ❌ issues found

---

#### `requirements.txt` (Python Dependencies)
**Purpose:** Lists all Python packages needed
**Contents:**
```
opencv-python>=4.5.0
pytesseract>=0.3.10
imutils>=0.5.4
numpy>=1.19.0
flask>=2.0.0
tabulate>=0.8.9
Werkzeug>=2.0.0
```

**Usage:**
```bash
pip install -r requirements.txt
```

---

### 📚 Documentation Files

#### `README.md` (Main Documentation)
**Purpose:** Complete project documentation
**Sections:**
- Features list
- Installation guide
- Usage instructions
- API documentation
- Best practices
- Troubleshooting
- Performance metrics

**Read this for:** Overall project understanding

---

#### `HOW_TO_RUN.md` (Setup & Execution Guide)
**Purpose:** Step-by-step guide to setup and run
**Sections:**
- First-time setup
- Running different applications
- Usage scenarios
- Troubleshooting
- Quick reference commands

**Read this for:** Getting the application running

---

#### `FILE_GUIDE.md` (This File)
**Purpose:** Navigate project structure and file purposes
**Contents:** File descriptions and organization

**Read this for:** Understanding project organization

---

### 🌐 Web Interface Files

#### `templates/index.html` (Web Interface)
**Purpose:** HTML interface for web application
**Features:**
- Drag-and-drop upload
- Method selection dropdown
- Language selection dropdown
- Real-time status updates
- Image previews
- Text editor
- Download functionality

**Served by:** Flask web_app.py

---

### 🪟 Windows Helper Files

#### `run.bat` (Windows Quick Start)
**Purpose:** Automated setup and execution for Windows
**Features:**
- Checks Python installation
- Creates virtual environment
- Installs dependencies
- Provides menu for common tasks

**Usage:**
```cmd
cd document-scanner-ocr
run.bat
```

---

## 📁 Working Directories

### Directory: `uploads/`
- **Created by:** web_app.py
- **Purpose:** Temporary storage of user uploads
- **Auto-cleanup:** Yes (can be configured)

### Directory: `processed_images/`
- **Created by:** web_app.py
- **Purpose:** Store processing pipeline results
- **Lifetime:** Per-scan (can be deleted after viewing)

### Directory: `output/`
- **Created by:** scanner.py, examples.py, cli.py
- **Purpose:** Final processing results
- **Contents:** Original, warped, and processed images

### Directory: `documents/` and `documents_batch/`
- **Created by:** examples.py
- **Purpose:** Sample documents for testing
- **Contains:** Test images for batch processing

### Directory: `templates/`
- **Purpose:** HTML templates for Flask
- **Contains:** index.html web interface

### Directory: `static/`
- **Purpose:** Static assets (CSS, JavaScript, images)
- **Status:** Currently empty (can be expanded)

### Directory: `venv/`
- **Created by:** `python -m venv venv`
- **Purpose:** Python virtual environment
- **Status:** Not tracked in version control

---

## 🔄 File Dependencies

```
document_scanner.py (No dependencies on other local files)
    ↓
    └─ Used by: scanner.py, cli.py, web_app.py, examples.py

config.py (Optional, can be imported by any file)

requirements.txt (Lists all pip dependencies)
    ↓ pip install
    ├─ opencv-python
    ├─ pytesseract
    ├─ imutils
    ├─ numpy
    ├─ flask
    └─ tabulate

web_app.py
    ├─ Imports: document_scanner
    └─ Serves: templates/index.html

templates/index.html
    └─ Served by: web_app.py
```

---

## 📊 File Statistics

| File | Lines | Type | Purpose |
|------|-------|------|---------|
| document_scanner.py | ~700 | Python | Core engine |
| cli.py | ~400 | Python | CLI tool |
| web_app.py | ~300 | Python | Web app |
| examples.py | ~450 | Python | Examples |
| scanner.py | ~80 | Python | Simple script |
| templates/index.html | ~400 | HTML | Web UI |
| config.py | ~100 | Python | Settings |
| quickstart.py | ~150 | Python | Setup check |
| README.md | ~800 | Markdown | Full docs |
| HOW_TO_RUN.md | ~700 | Markdown | Setup guide |
| requirements.txt | ~10 | Text | Dependencies |
| run.bat | ~50 | Batch | Windows helper |

**Total:** ~4,500+ lines of code and documentation

---

## 🚀 Quick File Usage Reference

### I want to...

| Goal | File(s) to Use |
|------|---|
| Scan one document quickly | `scanner.py` |
| Use command-line interface | `cli.py` |
| Use web interface | `web_app.py` + `templates/index.html` |
| See working examples | `examples.py` |
| Integrate into my code | `document_scanner.py` |
| Verify setup | `quickstart.py` |
| Understand everything | `README.md` |
| Get setup instructions | `HOW_TO_RUN.md` |
| Customize configuration | `config.py` |
| Windows quick start | `run.bat` |

---

## 🎨 Architecture Overview

```
┌─────────────────────────────────────────┐
│     USER INTERFACES                     │
├─────────────────────────────────────────┤
│ CLI (cli.py) │ Web (web_app.py) │ Script (scanner.py)
│              │         │         │
└──────────────┼─────────┼─────────┘
               │         │
               ▼         ▼
        ┌─────────────────────┐
        │  DocumentScanner    │ (document_scanner.py)
        │   (Core Engine)     │
        └─────────────────────┘
               │    │    │    │
        ┌──────┼────┼────┼────┴─────┐
        │      │    │    │          │
        ▼      ▼    ▼    ▼          ▼
    Detection Transform Enhance OCR Output
        (OpenCV, Tesseract)
```

---

## 📦 Installed Packages (via requirements.txt)

```
opencv-python       → Image processing
pytesseract         → OCR interface
imutils             → OpenCV utilities
numpy               → Array operations
flask               → Web framework
tabulate            → Table formatting
Werkzeug            → WSGI utilities
```

---

## 🔐 Security Notes

- **File uploads**: Limited to 16MB
- **Allowed formats**: JPG, PNG, BMP, TIFF only
- **Temporary storage**: Cleaned up after processing
- **File names**: Sanitized using `secure_filename()`

---

## 📝 Editing Files Guide

### To modify behavior:
1. **Preprocessing parameters** → Edit `config.py`
2. **CLI commands** → Edit `cli.py`
3. **Web interface** → Edit `templates/index.html`
4. **Core logic** → Edit `document_scanner.py`
5. **Web endpoints** → Edit `web_app.py`

### Before editing:
1. Back up original file
2. Read comments in file
3. Test changes thoroughly
4. Update documentation if needed

---

## 🆘 File Not Found Troubleshooting

| Missing File | Solution |
|---|---|
| `document_scanner.py` | Critical - restore from backup |
| `cli.py` | Re-download from repository |
| `requirements.txt` | Reinstall: `pip install -r requirements.txt` |
| `templates/index.html` | Web app won't work - restore file |
| `config.py` | Optional - recreate from backup |
| Generated folders | Will be created automatically |

---

**Version:** 1.0  
**Last Updated:** April 15, 2026  
**Status:** Complete ✓
