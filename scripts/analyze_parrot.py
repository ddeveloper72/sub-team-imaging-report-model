#!/usr/bin/env python3
"""
PARROT Dataset Analysis Script

This script analyzes the PARROT_v1_0.jsonl dataset to identify data elements 
present in real-world imaging reports and their usage patterns.

The script extracts and analyzes:
1. Report structure and content
2. Data element frequency
3. Language and modality patterns
4. Clinical finding patterns
5. Mapping to Xt-EHR model elements
"""

import json
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Tuple

class ParrotAnalyzer:
    """Analyzer for PARROT imaging reports dataset"""
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.reports = []
        self.analysis_results = {}
        
    def load_data(self) -> None:
        """Load JSONL data from file"""
        print(f"Loading data from {self.data_path}")
        with open(self.data_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    report = json.loads(line.strip())
                    self.reports.append(report)
                except json.JSONDecodeError as e:
                    print(f"Error parsing line {line_num}: {e}")
        
        print(f"Loaded {len(self.reports)} reports")
    
    def analyze_basic_structure(self) -> Dict[str, Any]:
        """Analyze basic structure and metadata of reports"""
        print("Analyzing basic report structure...")
        
        # Extract basic fields
        fields_present = Counter()
        languages = Counter()
        modalities = Counter()
        areas = Counter()
        countries = Counter()
        subspecialties = Counter()
        icd_codes = Counter()
        
        for report in self.reports:
            # Count which fields are present
            for field in report.keys():
                fields_present[field] += 1
            
            # Extract metadata
            if 'language' in report:
                languages[report['language']] += 1
            if 'modality' in report:
                modalities[report['modality']] += 1
            if 'area' in report:
                areas[report['area']] += 1
            if 'country' in report:
                countries[report['country']] += 1
            if 'subspecialty' in report:
                subspecialties[report['subspecialty']] += 1
            if 'icd' in report:
                # Handle multiple ICD codes
                icd_list = report['icd'].split(', ') if ',' in report['icd'] else [report['icd']]
                for icd in icd_list:
                    icd_codes[icd.strip()] += 1
        
        structure_analysis = {
            'total_reports': len(self.reports),
            'fields_present': dict(fields_present),
            'languages': dict(languages),
            'modalities': dict(modalities),
            'anatomical_areas': dict(areas),
            'countries': dict(countries),
            'subspecialties': dict(subspecialties),
            'icd_codes': dict(icd_codes)
        }
        
        return structure_analysis
    
    def analyze_report_content(self) -> Dict[str, Any]:
        """Analyze the actual report content for clinical elements"""
        print("Analyzing report content...")
        
        # Content analysis patterns
        report_lengths = []
        translation_lengths = []
        
        # Clinical patterns to look for
        clinical_patterns = {
            'findings_present': 0,
            'normal_reports': 0,
            'pathological_reports': 0,
            'comparison_mentioned': 0,
            'contrast_mentioned': 0,
            'measurements_present': 0,
            'recommendations_present': 0,
            'technique_described': 0
        }
        
        # Common clinical terms
        normal_terms = ['normal', 'unremarkable', 'sin particularidades', 'conservado', 'respetado']
        pathology_terms = ['lesion', 'abnormal', 'pathological', 'lesión', 'anormal', 'patológico']
        comparison_terms = ['comparison', 'compare', 'previous', 'prior', 'comparación', 'previo']
        contrast_terms = ['contrast', 'gadolinium', 'contraste', 'gadolinio']
        measurement_terms = ['mm', 'cm', 'size', 'diameter', 'tamaño', 'diámetro']
        recommendation_terms = ['recommend', 'suggest', 'follow', 'recomienda', 'sugiere', 'seguimiento']
        
        for report in self.reports:
            # Analyze report content
            report_text = report.get('report', '')
            translation_text = report.get('translation', '')
            
            report_lengths.append(len(report_text))
            if translation_text:
                translation_lengths.append(len(translation_text))
            
            # Combine report and translation for analysis
            full_text = (report_text + ' ' + translation_text).lower()
            
            # Check for clinical patterns
            if any(term in full_text for term in normal_terms):
                clinical_patterns['normal_reports'] += 1
            if any(term in full_text for term in pathology_terms):
                clinical_patterns['pathological_reports'] += 1
            if any(term in full_text for term in comparison_terms):
                clinical_patterns['comparison_mentioned'] += 1
            if any(term in full_text for term in contrast_terms):
                clinical_patterns['contrast_mentioned'] += 1
            if any(term in full_text for term in measurement_terms):
                clinical_patterns['measurements_present'] += 1
            if any(term in full_text for term in recommendation_terms):
                clinical_patterns['recommendations_present'] += 1
            
            # Check for findings vs normal
            if report_text:
                clinical_patterns['findings_present'] += 1
        
        content_analysis = {
            'report_length_stats': {
                'mean': np.mean(report_lengths),
                'median': np.median(report_lengths),
                'min': min(report_lengths),
                'max': max(report_lengths)
            },
            'translation_length_stats': {
                'mean': np.mean(translation_lengths) if translation_lengths else 0,
                'median': np.median(translation_lengths) if translation_lengths else 0,
                'min': min(translation_lengths) if translation_lengths else 0,
                'max': max(translation_lengths) if translation_lengths else 0
            } if translation_lengths else None,
            'clinical_patterns': clinical_patterns
        }
        
        return content_analysis
    
    def map_to_xt_ehr_elements(self) -> Dict[str, Any]:
        """Map PARROT data elements to Xt-EHR model elements"""
        print("Mapping to Xt-EHR elements...")
        
        # Mapping of PARROT fields to Xt-EHR elements
        xt_ehr_mapping = {
            # Header elements that are definitely present
            'present_required': {
                'header.subject': 'Implied by report existence',
                'header.documentType': 'Implied as imaging report',
                'header.documentTitle': 'Can be derived from modality + area',
                'body.examinationReport.modality': 'Directly available in modality field',
                'body.examinationReport.conclusion.impression': 'Available in report/translation field'
            },
            
            # Header elements that could be derived
            'derivable': {
                'header.language': 'Available in language field',
                'header.authorship.author': 'Available in contributor_code field',
                'header.serviceSpecialty': 'Available in subspecialty field',
                'body.examinationReport.bodyPart': 'Available in area field'
            },
            
            # Clinical elements found in content
            'content_derived': {
                'body.examinationReport.resultData.resultText': 'Full report text',
                'body.examinationReport.conclusion.conditionOrFinding': 'ICD codes provide structured findings',
                'body.supportingInformation.condition': 'Can be derived from clinical context',
                'body.comparisonStudy': 'When comparison studies mentioned',
                'body.examinationReport.medication': 'When contrast agents mentioned',
                'body.recommendation': 'When recommendations present in text'
            },
            
            # Elements rarely or never present
            'rarely_present': {
                'header.identifier': 'No unique document identifiers',
                'header.authorship.datetime': 'No timestamps available',
                'header.status': 'No status information',
                'header.accessionNumber': 'No accession numbers',
                'header.healthInsuranceAndPaymentInformation': 'No insurance data',
                'body.orderInformation': 'No order information',
                'body.exposureInformation': 'No radiation dose information',
                'body.specimen': 'Limited specimen information',
                'dicomStudyMetadata': 'No DICOM metadata',
                'attachments': 'No file attachments'
            }
        }
        
        # Calculate presence statistics
        presence_stats = {}
        total_reports = len(self.reports)
        
        # Count actual occurrences in the dataset
        for category, elements in xt_ehr_mapping.items():
            presence_stats[category] = {}
            for element, description in elements.items():
                if category == 'present_required':
                    presence_stats[category][element] = {'count': total_reports, 'percentage': 100.0}
                elif category == 'derivable':
                    # Check actual field presence
                    if 'language' in element:
                        count = sum(1 for r in self.reports if 'language' in r and r['language'])
                    elif 'contributor_code' in element:
                        count = sum(1 for r in self.reports if 'contributor_code' in r and r['contributor_code'])
                    elif 'subspecialty' in element:
                        count = sum(1 for r in self.reports if 'subspecialty' in r and r['subspecialty'])
                    elif 'area' in element:
                        count = sum(1 for r in self.reports if 'area' in r and r['area'])
                    else:
                        count = 0
                    presence_stats[category][element] = {
                        'count': count, 
                        'percentage': (count / total_reports) * 100
                    }
                else:
                    # For content-derived and rarely present, use content analysis
                    presence_stats[category][element] = {
                        'count': 0, 
                        'percentage': 0.0,
                        'description': description
                    }
        
        return {
            'mapping': xt_ehr_mapping,
            'presence_statistics': presence_stats
        }
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run complete analysis pipeline"""
        print("Starting complete PARROT dataset analysis...")
        
        # Load data
        self.load_data()
        
        # Run all analyses
        structure_analysis = self.analyze_basic_structure()
        content_analysis = self.analyze_report_content()
        mapping_analysis = self.map_to_xt_ehr_elements()
        
        # Compile results
        self.analysis_results = {
            'dataset_info': {
                'total_reports': len(self.reports),
                'source_file': str(self.data_path)
            },
            'structure_analysis': structure_analysis,
            'content_analysis': content_analysis,
            'xt_ehr_mapping': mapping_analysis
        }
        
        return self.analysis_results
    
    def save_results(self, output_path: str) -> None:
        """Save analysis results to JSON file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        
        print(f"Analysis results saved to {output_file}")
    
    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report"""
        if not self.analysis_results:
            return "No analysis results available. Run analysis first."
        
        report_lines = []
        report_lines.append("# PARROT Dataset Analysis Summary")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        # Dataset overview
        total_reports = self.analysis_results['dataset_info']['total_reports']
        report_lines.append(f"## Dataset Overview")
        report_lines.append(f"- Total Reports: {total_reports}")
        report_lines.append("")
        
        # Structure analysis
        structure = self.analysis_results['structure_analysis']
        report_lines.append("## Data Structure Analysis")
        report_lines.append(f"- Languages: {len(structure['languages'])} different languages")
        report_lines.append(f"- Modalities: {len(structure['modalities'])} different modalities")
        report_lines.append(f"- Anatomical Areas: {len(structure['anatomical_areas'])} different areas")
        report_lines.append(f"- Countries: {len(structure['countries'])} different countries")
        report_lines.append("")
        
        # Top frequencies
        report_lines.append("### Most Common:")
        report_lines.append(f"- Language: {max(structure['languages'], key=structure['languages'].get)}")
        report_lines.append(f"- Modality: {max(structure['modalities'], key=structure['modalities'].get)}")
        report_lines.append(f"- Area: {max(structure['anatomical_areas'], key=structure['anatomical_areas'].get)}")
        report_lines.append("")
        
        # Content analysis
        content = self.analysis_results['content_analysis']
        clinical = content['clinical_patterns']
        report_lines.append("## Clinical Content Analysis")
        report_lines.append(f"- Normal Reports: {clinical['normal_reports']} ({clinical['normal_reports']/total_reports*100:.1f}%)")
        report_lines.append(f"- Pathological Reports: {clinical['pathological_reports']} ({clinical['pathological_reports']/total_reports*100:.1f}%)")
        report_lines.append(f"- Comparison Studies: {clinical['comparison_mentioned']} ({clinical['comparison_mentioned']/total_reports*100:.1f}%)")
        report_lines.append(f"- Contrast Use: {clinical['contrast_mentioned']} ({clinical['contrast_mentioned']/total_reports*100:.1f}%)")
        report_lines.append(f"- Measurements: {clinical['measurements_present']} ({clinical['measurements_present']/total_reports*100:.1f}%)")
        report_lines.append(f"- Recommendations: {clinical['recommendations_present']} ({clinical['recommendations_present']/total_reports*100:.1f}%)")
        report_lines.append("")
        
        # Xt-EHR mapping
        mapping = self.analysis_results['xt_ehr_mapping']
        report_lines.append("## Xt-EHR Element Mapping")
        report_lines.append(f"- Always Present Elements: {len(mapping['mapping']['present_required'])}")
        report_lines.append(f"- Derivable Elements: {len(mapping['mapping']['derivable'])}")
        report_lines.append(f"- Content-Derived Elements: {len(mapping['mapping']['content_derived'])}")
        report_lines.append(f"- Rarely Present Elements: {len(mapping['mapping']['rarely_present'])}")
        report_lines.append("")
        
        return "\\n".join(report_lines)


def main():
    """Main execution function"""
    # Set up paths
    data_path = "c:/Users/duncanfalconer/VS_Code_Projects/FHIR Imaging Report/data/PARROT_v1_0.jsonl"
    output_path = "c:/Users/duncanfalconer/VS_Code_Projects/FHIR Imaging Report/output/parrot_analysis.json"
    summary_path = "c:/Users/duncanfalconer/VS_Code_Projects/FHIR Imaging Report/output/parrot_summary.md"
    
    # Run analysis
    analyzer = ParrotAnalyzer(data_path)
    results = analyzer.run_complete_analysis()
    
    # Save results
    analyzer.save_results(output_path)
    
    # Generate and save summary
    summary = analyzer.generate_summary_report()
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"Analysis complete!")
    print(f"Results saved to: {output_path}")
    print(f"Summary saved to: {summary_path}")
    
    # Print summary to console
    print("\\n" + summary)


if __name__ == "__main__":
    main()