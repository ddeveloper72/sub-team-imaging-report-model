# Xt-EHR T7.2 Sub-team for Imaging Reports Model Analysis

[![Deploy Status](https://img.shields.io/badge/deploy-success-brightgreen)](https://sub-team-imaging-report-model-984bf6c1ddb8.herokuapp.com/) [![Live Demo](https://img.shields.io/badge/demo-live-blue)](https://sub-team-imaging-report-model-984bf6c1ddb8.herokuapp.com/)


## Live Analysis Dashboard

The dashboard provides:
- Interactive data element usage statistics
- Real-world vs. model element mappings
- Detailed analysis results and recommendations
- Downloadable reports and visualizations

## Overview
This project analyzes the Xt-EHR Imaging Report information model to identify data elements used in reality versus those that could be considered "beyond basic" by comparing with real-world imaging reports from the PARROT dataset.

## Project Structure

- `docs/` - Documentation and extracted model definitions
- `analysis/` - Analysis scripts and results  
- `data/` - Processed data files and extracts
- `scripts/` - Utility scripts for data processing
- `output/` - Final analysis results and reports
- `flask_app/` - Web application for viewing results (see flask_app/README.md)
- `PARROT_v1_0.jsonl` - Source dataset of real imaging reports

## Goals

1. Extract all data elements from Xt-EHR Imaging Report and Study models
2. Analyze real-world usage patterns from PARROT dataset
3. Map real-world elements to Xt-EHR model elements
4. Identify candidates for "beyond basic" classification
5. Generate recommendations for basic vs. beyond basic categorization

## Data Sources

- **Xt-EHR Information Model**: https://build.fhir.org/ig/Xt-EHR/xt-ehr-common/
  - Imaging Report: https://build.fhir.org/ig/Xt-EHR/xt-ehr-common/StructureDefinition-EHDSImagingReport.html
  - Imaging Study: https://build.fhir.org/ig/Xt-EHR/xt-ehr-common/StructureDefinition-EHDSImagingStudy.html
- **PARROT Dataset v1.0**: Real-world imaging reports in multiple languages with ICD codes
  - Source: https://github.com/PARROT-reports/PARROT_v1.0
  - Description: Multi-language dataset of real-world radiology reports for research purposes

## Analysis Approach

1. **Model Extraction**: Parse Xt-EHR models to identify all data elements with cardinality
2. **Real-world Analysis**: Process PARROT reports to identify present data patterns
3. **Usage Mapping**: Map real-world patterns to model elements
4. **Gap Analysis**: Identify unused or rarely used elements
5. **Categorization**: Recommend basic vs. beyond basic classifications

## Key Findings

Based on analysis of 2,738 real-world imaging reports:

- **11 core elements** provide 90%+ coverage of real-world usage
- **31+ additional elements** identified as "beyond basic" candidates
- **Detailed mappings** available in analysis documents

## Web Interface

A Flask web application is available for viewing analysis results:

```bash
cd flask_app
python app.py
```

See `flask_app/README.md` for detailed setup and deployment instructions.

## Development Environment

### Prerequisites
- Python 3.12+
- Git

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd "FHIR Imaging Report"

# For web app setup, see flask_app/README.md
```

## Team

Xt-EHR T7.2 Sub-team for Imaging Reports Model

## Acknowledgments

This project builds upon the work of several important initiatives:

### PARROT Project
- **Source**: https://github.com/PARROT-reports/PARROT_v1.0
- **Contribution**: The PARROT v1.0 dataset provides the real-world imaging reports that form the foundation of our analysis. This multi-language dataset of radiology reports enables evidence-based assessment of data element usage patterns.
- **Citation**: PARROT v1.0 - A multi-language dataset of real-world radiology reports for research purposes.

### Xt-EHR Project
- **Source**: https://build.fhir.org/ig/Xt-EHR/xt-ehr-common/index.html
- **Contribution**: The Xt-EHR FHIR Implementation Guide provides the imaging report and study data models that are analyzed in this project. The comprehensive information models enable structured comparison with real-world usage patterns.
- **Citation**: Xt-EHR FHIR Implementation Guide - Common profiles and extensions for cross-border health data exchange.

We gratefully acknowledge the contributions of both projects in enabling this comparative analysis and the advancement of standardized health data exchange.

## License

This project is part of the Xt-EHR T7.2 Sub-team analysis work.