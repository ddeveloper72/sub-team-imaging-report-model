# Xt-EHR T7.2 Sub-team for Imaging Reports Model Analysis

[![Deploy Status](https://img.shields.io/badge/deploy-success-brightgreen)](https://sub-team-imaging-report-model-984bf6c1ddb8.herokuapp.com/) [![Analysis For Review](https://img.shields.io/badge/analysis-for_review-blue)](https://sub-team-imaging-report-model-984bf6c1ddb8.herokuapp.com/)

## Original Project Request

**Prompt**: *"Analyze the Xt-EHR Imaging Report information model to identify which data elements are actually used in real-world imaging reports versus those that could be considered 'beyond basic' by comparing with real-world imaging reports from the PARROT dataset."*

### Specific Requirements:
1. **Extract all data elements** from Xt-EHR Imaging Report and Study models
2. **Analyze real-world usage patterns** from PARROT dataset  
3. **Map real-world elements** to Xt-EHR model elements
4. **Identify candidates** for "beyond basic" classification
5. **Generate recommendations** for basic vs. beyond basic categorization

## Live Analysis Dashboard

The dashboard provides:
- Interactive data element usage statistics
- Real-world vs. model element mappings
- Detailed analysis results and recommendations
- Downloadable reports and visualizations

## Overview

This project provides evidence-based analysis of the **Xt-EHR Imaging Report information model** by comparing theoretical model elements against real-world usage patterns from the **PARROT dataset**. Our goal is to identify which data elements are essential for core clinical workflows versus those serving specialized administrative or technical functions.

### 🤖 AI Analysis Attribution

**In accordance with EU AI Act transparency requirements (Article 52):**

> **AI-Assisted Analysis**: The data analysis, pattern identification, and report compilation in this project were performed with the assistance of **Claude Sonnet 4.5** (Anthropic), a large language model and General-Purpose AI system. All findings have been validated against source data from the PARROT v1.0 dataset and Xt-EHR model specifications, and are subject to expert review by the Xt-EHR T7.2 Sub-team.

**Scope of AI Involvement**:
- Analysis of 2,738 real-world imaging reports from PARROT v1.0 dataset
- Pattern recognition and element usage frequency calculations
- Comparative mapping between real-world data and Xt-EHR model specifications
- Classification recommendations (Basic, Intermediate, Beyond Basic categories)
- Documentation synthesis and report generation

**Human Oversight**: All AI-generated analysis and recommendations undergo expert validation and are reviewed within the context of healthcare interoperability standards and clinical practice.

**📖 Compliance Resources**:
- [EU AI Act Compliance Statement](docs/EU-AI-ACT-COMPLIANCE.md) - Full regulatory compliance documentation
- [AI Attribution Quick Reference](docs/AI-ATTRIBUTION-QUICK-REFERENCE.md) - Attribution templates and FAQ

## Analysis Methodology

### 🔄 Process Flow

```mermaid
graph TB
    subgraph "Data Sources"
        A[Xt-EHR FHIR IG v0.2.1<br/>EHDS Information Models]
        B[PARROT v1.0 Dataset<br/>2,738 Real Reports]
    end
    
    subgraph "Model Extraction"
        C[Extract Data Elements<br/>Header & Body Structure]
        D[Classify Element Types<br/>Required vs Optional]
    end
    
    subgraph "Real-World Analysis"
        E[Parse Report Content<br/>14 Languages, 21 Countries]
        F[Identify Usage Patterns<br/>Modality, Anatomy, Findings]
    end
    
    subgraph "Comparative Analysis"
        G[Map Real-World to Model<br/>Element Usage Frequency]
        H[Gap Analysis<br/>Used vs Unused Elements]
    end
    
    subgraph "Evidence-Based Classification"
        I[BASIC Elements<br/>11 Core Elements - 90%+ Value]
        J[INTERMEDIATE Elements<br/>6 Enhanced Workflow Elements]
        K[BEYOND BASIC Elements<br/>31+ Admin/Technical Elements]
    end
    
    A --> C
    A --> D
    B --> E
    B --> F
    C --> G
    D --> G
    E --> G
    F --> G
    G --> H
    H --> I
    H --> J
    H --> K
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style I fill:#c8e6c9
    style J fill:#fff3e0
    style K fill:#ffebee
```

### 📊 Data Source References

#### Xt-EHR FHIR Implementation Guide
- **Current Version**: [v0.2.1 (October 10, 2025)](https://www.xt-ehr.eu/fhir/models/history.html)
- **Main Repository**: [Xt-EHR/xt-ehr-common](https://github.com/Xt-EHR/xt-ehr-common)
- **Issue Tracking**: [GitHub Issues](https://github.com/Xt-EHR/xt-ehr-common/issues)
- **Imaging Report Model**: [EHDSImagingReport](https://github.com/xt-ehr/xt-ehr-common/tree/main/input/fsh/EHDS-models/imagingReport.fsh)
- **Imaging Study Model**: [EHDSImagingStudy](https://github.com/xt-ehr/xt-ehr-common/tree/main/input/fsh/EHDS-models/imagingStudy.fsh)

#### PARROT Dataset
- **Source Repository**: [PARROT v1.0](https://github.com/PARROT-reports/PARROT_v1.0)
- **Dataset Scope**: 2,738 real-world imaging reports
- **Coverage**: 14 languages, 21 countries, 10 imaging modalities
- **Data Elements**: Clinical narratives, ICD codes, modality classifications

### 🔗 Model Traceability

Our analysis directly references specific elements from the Xt-EHR models:

| Model Section | FHIR Path | Analysis Coverage |
|---------------|-----------|-------------------|
| **Header Elements** | `EHDSImagingReport.header.*` | Document metadata, authorship, recipients |
| **Order Information** | `EHDSImagingReport.body.orderInformation.*` | Service requests, clinical context |
| **Examination Report** | `EHDSImagingReport.body.examinationReport.*` | Modality, anatomy, procedures, findings |
| **Supporting Info** | `EHDSImagingReport.body.supportingInformation.*` | Clinical context, medications, devices |
| **Study Metadata** | `EHDSImagingStudy.*` | DICOM metadata, series information |

## Data Sources

### 🏛️ Xt-EHR Information Model
- **Official Site**: [Xt-EHR Project](https://www.xt-ehr.eu/)
- **FHIR Implementation Guide**: [EHDS Logical Information Models](https://www.xt-ehr.eu/fhir/models/history.html)
- **Current Version**: v0.2.1 (October 10, 2025) - *First preview version of EHDS Logical Information Models*
- **Development Repository**: [Xt-EHR/xt-ehr-common](https://github.com/Xt-EHR/xt-ehr-common)
- **Imaging Components**:
  - [Imaging Report Model](https://github.com/xt-ehr/xt-ehr-common/tree/main/input/fsh/EHDS-models/imagingReport.fsh): Comprehensive diagnostic report structure
  - [Imaging Study Model](https://github.com/xt-ehr/xt-ehr-common/tree/main/input/fsh/EHDS-models/imagingStudy.fsh): DICOM study metadata and organization

### 📊 PARROT Dataset v1.0
- **Source Repository**: [PARROT-reports/PARROT_v1.0](https://github.com/PARROT-reports/PARROT_v1.0)
- **Dataset Characteristics**:
  - **Volume**: 2,738 real-world imaging reports
  - **Geographic Coverage**: 21 countries across Europe
  - **Language Diversity**: 14 languages
  - **Modality Coverage**: 10 imaging types (CT, MRI, X-ray, etc.)
  - **Clinical Context**: Full diagnostic narratives with ICD code classifications
- **Research Purpose**: Multi-language dataset enabling evidence-based assessment of imaging report structures

## Project Structure

- `docs/` - Documentation and extracted model definitions
- `analysis/` - Analysis scripts and results  
- `data/` - Processed data files and extracts (PARROT_v1_0.jsonl)
- `scripts/` - Utility scripts for data processing
- `output/` - Final analysis results and reports
- `flask_app/` - Web application for viewing results (see flask_app/README.md)

## Key Findings

Based on comprehensive analysis of **2,738 real-world imaging reports** against the **Xt-EHR v0.2.1 model specification**:

### 📈 Usage Statistics
- **11 core elements** provide 90%+ coverage of real-world clinical value
- **31+ additional elements** identified as "beyond basic" candidates  
- **100% coverage** of essential clinical content (narratives, modalities, anatomy)
- **0% coverage** of administrative metadata in real-world reports

### 🎯 Evidence-Based Classification
| Category | Element Count | Clinical Coverage | Implementation Complexity |
|----------|---------------|-------------------|---------------------------|
| **BASIC** | 11 elements | 90%+ clinical value | Low - immediate interoperability |
| **INTERMEDIATE** | 6 elements | Enhanced workflows | Medium - use case driven |
| **BEYOND BASIC** | 31+ elements | Administrative/technical | High - specialized requirements |

### 🔍 Detailed Mappings
Available in analysis documents with complete traceability to source models and real-world evidence.

## Web Interface

A Flask web application provides interactive access to all analysis results:

```bash
cd flask_app
python app.py
```

**Features**:
- Document library with search and categorization
- Mobile-first responsive design  
- PDF export with selectable orientations
- Real-time analysis dashboard

See `flask_app/README.md` for detailed setup and deployment instructions.

## Implementation Strategy

### 📋 Phase 1: Basic Profile (Recommended Start)
**Target**: Core 11 elements for immediate clinical value
- **Complexity**: Low implementation burden
- **Coverage**: 90%+ of real-world clinical needs  
- **ROI**: Very high - maximum value with minimal effort

### 🔧 Phase 2: Enhanced Profile (Use Case Driven)
**Target**: Additional 6 intermediate elements
- **Complexity**: Medium - specific workflow integration
- **Coverage**: Enhanced clinical context and workflows
- **ROI**: Medium-High - targeted value for specific use cases

### 🏢 Phase 3: Comprehensive Profile (Enterprise/Regulatory)
**Target**: Full model implementation including beyond basic elements
- **Complexity**: High - complete administrative and technical infrastructure
- **Coverage**: Full workflow support and regulatory compliance
- **ROI**: Low-Medium - justified only for specialized institutional needs

## Regulatory Compliance

### 🇪🇺 EU AI Act Compliance

This project operates in accordance with the **European Union Artificial Intelligence Act** [(Regulation EU 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), which establishes harmonized rules for trustworthy AI in Europe.

**Classification**: Limited Risk (Transparency Requirements)
- AI-assisted analysis for healthcare data model evaluation
- Transparency obligations fulfilled through clear AI attribution
- Subject to human oversight and expert validation

**Key Resources**:
- 📋 [EU AI Act - European Commission](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- 🇮🇪 [Irish Implementation - Enterprise Ireland](https://enterprise.gov.ie/en/what-we-do/innovation-research-development/artificial-intelligence/eu-ai-act/)
- 🏛️ [European Approach to AI](https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence)
- 📖 [Project Compliance Statement](docs/EU-AI-ACT-COMPLIANCE.md) - Detailed compliance documentation

**Timeline Context**:
- AI Act entered into force: 2 August 2024
- Transparency requirements (Article 52): In effect
- GPAI obligations: 2 August 2025
- Full application: 2 August 2026

This project aligns with the **European Health Data Space (EHDS)** initiative and supports trustworthy AI principles in healthcare interoperability.

---

## Acknowledgments

This project builds upon the work of several important initiatives:

### 🏛️ Xt-EHR Project  
- **Source**: [Xt-EHR Official Site](https://www.xt-ehr.eu/) | [GitHub Repository](https://github.com/Xt-EHR/xt-ehr-common)
- **Version Analyzed**: [v0.2.1 (October 10, 2025)](https://www.xt-ehr.eu/fhir/models/history.html)
- **Contribution**: The Xt-EHR FHIR Implementation Guide provides the comprehensive imaging report data model that serves as the basis for this classification analysis. The detailed specification enables systematic comparison with real-world usage patterns and supports evidence-based implementation guidance.
- **Reference**: *Xt-EHR Joint Action - EHDS Logical Information Models for cross-border health data exchange*

### 📊 PARROT Project
- **Source**: [PARROT v1.0 Dataset](https://github.com/PARROT-reports/PARROT_v1.0)
- **Contribution**: The PARROT v1.0 dataset provides the foundational real-world data for this analysis. This comprehensive collection of 2,738 multi-language imaging reports across 14 languages and 21 countries enables evidence-based assessment of actual clinical usage patterns.
- **Reference**: *PARROT v1.0 - A multi-language dataset of real-world radiology reports for research purposes*

### 🤖 AI Analysis Tools
- **Model**: Claude Sonnet 4.5 (Anthropic)
- **Classification**: General-Purpose AI (GPAI) Model under EU AI Act
- **Role**: AI-assisted data analysis, pattern recognition, and report compilation
- **Governance**: Subject to EU AI Act transparency requirements and human oversight
- **Contribution**: Enabled efficient analysis of large-scale dataset (2,738 reports) with comprehensive pattern identification and automated documentation generation

### 🔗 Model Provenance
Our analysis maintains full traceability to source materials:
- **Xt-EHR Elements**: Direct references to [FSH model definitions](https://github.com/xt-ehr/xt-ehr-common/tree/main/input/fsh/EHDS-models/)
- **Real-World Evidence**: Quantitative analysis of PARROT dataset usage patterns
- **AI-Assisted Classification**: Evidence-based justification validated by domain experts
- **Regulatory Compliance**: Aligned with EU AI Act and EHDS frameworks

We gratefully acknowledge the contributions of all projects and tools in enabling this comparative analysis and advancing standardized, trustworthy health data exchange.

## License

This project is part of the Xt-EHR T7.2 Sub-team analysis work.

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