# Xt-EHR Imaging Report Analysis Project

## Overview
This project analyzes the Xt-EHR Imaging Report information model to identify data elements used in reality versus those that could be considered "beyond basic" by comparing with real-world imaging reports from the PARROT dataset.

## Project Structure

- `docs/` - Documentation and extracted model definitions
- `analysis/` - Analysis scripts and notebooks
- `data/` - Processed data files and extracts
- `scripts/` - Utility scripts for data processing
- `output/` - Final analysis results and reports
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
- **PARROT Dataset**: Real-world imaging reports in multiple languages with ICD codes

## Analysis Approach

1. **Model Extraction**: Parse Xt-EHR models to identify all data elements with cardinality
2. **Real-world Analysis**: Process PARROT reports to identify present data patterns
3. **Usage Mapping**: Map real-world patterns to model elements
4. **Gap Analysis**: Identify unused or rarely used elements
5. **Categorization**: Recommend basic vs. beyond basic classifications