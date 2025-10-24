# Xt-EHR T7.2 Sub-team for Imaging Reports Model Analysis

## Overview
This project analyzes the Xt-EHR Imaging Report information model to identify data elements used in reality versus those that could be considered "beyond basic" by comparing with real-world imaging reports from the PARROT dataset.

The project includes a **Flask web application** with mobile-first design for viewing analysis results and generating professional PDF reports with user-selectable orientations.

## 🚀 Quick Start

### Prerequisites
- Python 3.12 or higher
- Git

### Installation & Setup

#### Windows (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd "FHIR Imaging Report"

# Run the setup script
setup.bat
```

#### Unix/macOS/Linux
```bash
# Clone the repository
git clone <repository-url>
cd "FHIR Imaging Report"

# Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

#### Manual Setup
```bash
# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Unix/macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the application
cd flask_app
python app.py
```

### 🌐 Web Application Features

- **Mobile-First Design**: Responsive interface optimized for all devices
- **Document Library**: Browse and view analysis documents with markdown rendering
- **PDF Generation**: Export individual documents or bulk collections as PDFs
- **Orientation Selection**: Choose Portrait or Landscape PDF layouts
- **Dynamic Styling**: Professional HCO color scheme with adaptive font sizing
- **Bulk Operations**: Select multiple documents for combined PDF exports

Access the application at: `http://localhost:5000`

## 📁 Project Structure

```
├── flask_app/          # Web application
│   ├── app.py         # Main Flask application
│   ├── templates/     # HTML templates
│   └── static/        # CSS, JS, assets
├── docs/              # Documentation and model definitions
├── analysis/          # Analysis scripts and results
├── data/              # Processed data files
├── scripts/           # Utility scripts
├── output/            # Final analysis results
├── requirements.txt   # Core dependencies
├── requirements-dev.txt   # Development dependencies
├── requirements-prod.txt  # Production dependencies
├── setup.bat         # Windows setup script
├── setup.sh          # Unix setup script
└── PARROT_v1_0.jsonl # Source dataset
```

## 🎯 Goals

1. Extract all data elements from Xt-EHR Imaging Report and Study models
2. Analyze real-world usage patterns from PARROT dataset
3. Map real-world elements to Xt-EHR model elements
4. Identify candidates for "beyond basic" classification
5. Generate recommendations for basic vs. beyond basic categorization
6. Provide accessible web interface for results visualization

## 📊 Data Sources

- **Xt-EHR Information Model**: https://build.fhir.org/ig/Xt-EHR/xt-ehr-common/
  - Imaging Report: https://build.fhir.org/ig/Xt-EHR/xt-ehr-common/StructureDefinition-EHDSImagingReport.html
  - Imaging Study: https://build.fhir.org/ig/Xt-EHR/xt-ehr-common/StructureDefinition-EHDSImagingStudy.html
- **PARROT Dataset**: Real-world imaging reports in multiple languages with ICD codes

## 🔬 Analysis Approach

1. **Model Extraction**: Parse Xt-EHR models to identify all data elements with cardinality
2. **Real-world Analysis**: Process PARROT reports to identify present data patterns
3. **Usage Mapping**: Map real-world patterns to model elements
4. **Gap Analysis**: Identify unused or rarely used elements
5. **Categorization**: Recommend basic vs. beyond basic classifications

## 🛠️ Technical Stack

- **Backend**: Flask 3.0.0 with Python 3.12
- **PDF Generation**: ReportLab 4.4.4 with dynamic orientation support
- **Markdown Processing**: Python-Markdown 3.5.1
- **Frontend**: Bootstrap 5.3.0 with mobile-first responsive design
- **Icons**: Font Awesome 6.4.0
- **Color Scheme**: Professional healthcare organization palette

## 📄 Dependencies

### Core Dependencies (requirements.txt)
- Flask 3.0.0 - Web framework
- ReportLab 4.4.4 - PDF generation
- Markdown 3.5.1 - Document processing
- Werkzeug, Jinja2, MarkupSafe - Flask ecosystem

### Development Dependencies (requirements-dev.txt)
- pytest - Testing framework
- black, flake8 - Code formatting and linting
- mkdocs - Documentation generation

### Production Dependencies (requirements-prod.txt)
- gunicorn - WSGI server
- whitenoise - Static file serving

## 🎨 Key Features

### PDF Generation
- **Dynamic Orientation**: Portrait for text-heavy documents, Landscape for wide tables
- **Adaptive Sizing**: Font sizes automatically adjust based on orientation
- **Professional Layout**: HCO-branded headers, footers, and document separators
- **Text Wrapping**: Proper handling of long content in table cells
- **Bulk Operations**: Combine multiple documents with table of contents

### Mobile-First Design
- **Responsive Tables**: Stack on mobile, tabular on desktop
- **Touch-Friendly**: Large buttons and intuitive navigation
- **Progressive Enhancement**: Works without JavaScript
- **Fast Loading**: Optimized for low-bandwidth connections

## 🚀 Development

### Running in Development Mode
```bash
cd flask_app
python app.py
```

### Installing Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### Running Tests (when available)
```bash
pytest
```

## 📝 License

This project is part of the Xt-EHR T7.2 Sub-team for Imaging Reports Model analysis.

## 🤝 Contributing

This is an analysis project for the Xt-EHR T7.2 Sub-team. Please coordinate with the team lead for contributions.