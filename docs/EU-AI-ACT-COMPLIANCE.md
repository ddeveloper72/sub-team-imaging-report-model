# EU AI Act Compliance Statement

**Project**: Xt-EHR Imaging Report Elements Analysis  
**Document Version**: 1.0  
**Last Updated**: November 2025  
**Framework Reference**: [EU Artificial Intelligence Act (Regulation EU 2024/1689)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689)

---

## 1. Project Classification Under EU AI Act

### 1.1 AI System Classification

This project involves the use of **AI-assisted analysis** for healthcare data model evaluation. Under the EU AI Act risk-based framework:

#### **Risk Category**: Limited Risk (Transparency Requirements)
- This project uses generative AI (Claude Sonnet 4.5) for data analysis and report compilation
- The AI system operates in a **transparency-required** context per Article 52 of the AI Act
- The project involves healthcare-related data but does not directly impact patient care or clinical decision-making

#### **Not Classified As**:
- ❌ **High-Risk AI System** - The analysis does not directly:
  - Make clinical decisions or diagnoses
  - Assess patient health or safety
  - Control medical devices or diagnostic systems
  - Impact access to healthcare services
  
- ❌ **Unacceptable Risk** - The project does not involve:
  - Biometric categorization or emotion recognition
  - Social scoring or predictive policing
  - Manipulation or exploitation techniques

### 1.2 Project Purpose and Scope

**Primary Function**: Evidence-based analysis of healthcare data models to support standardization and interoperability within the European Health Data Space (EHDS).

**AI Usage**: 
- AI-assisted data analysis and pattern recognition
- Automated classification and categorization
- Report compilation and synthesis
- Documentation generation

**Human Oversight**: All AI-generated analysis is subject to expert review and validation by the Xt-EHR T7.2 Sub-team.

---

## 2. EU AI Act Transparency Compliance

### 2.1 AI-Generated Content Disclosure

**In accordance with Article 52(1) of the EU AI Act**, this project makes the following transparency declarations:

#### 2.1.1 AI Analysis Attribution

**AI System Used**: 
- **Model**: Claude Sonnet 4.5 (Anthropic)
- **Classification**: Large Language Model (LLM) / General-Purpose AI Model
- **Role**: Data analysis, pattern identification, report compilation, and documentation synthesis

**Scope of AI Involvement**:
- ✅ Analysis of PARROT v1.0 dataset (2,738 imaging reports)
- ✅ Identification of data element usage patterns
- ✅ Comparative analysis against Xt-EHR model specifications
- ✅ Classification of elements (Basic, Intermediate, Beyond Basic)
- ✅ Report compilation and documentation generation
- ✅ Statistical analysis and data visualization recommendations

**Human Expert Review**:
- All AI-generated findings are reviewed by domain experts
- Final recommendations are validated against source data
- Implementation guidance is subject to stakeholder consultation

#### 2.1.2 Content Marking

All project documentation includes clear attribution stating:

> **AI Analysis Attribution**: The analysis and reports in this project were compiled with the assistance of Claude Sonnet 4.5, an AI language model by Anthropic. All findings have been validated against source data and are subject to expert review.

---

## 3. Healthcare Context and EHDS Alignment

### 3.1 European Health Data Space (EHDS) Context

This project supports the implementation of the **European Health Data Space (EHDS)**, which operates in coordination with the EU AI Act:

**EHDS Objectives**:
- Enable secure cross-border health data exchange
- Support primary use (patient care) and secondary use (research) of health data
- Establish common standards for health data interoperability

**AI Act Alignment**:
- Healthcare AI systems are subject to specific requirements under Annex III of the AI Act
- This project provides foundational analysis to support compliant implementation
- Focus on trustworthy AI principles: transparency, accountability, human oversight

### 3.2 Data Privacy and Security

**GDPR Compliance**:
- Analysis uses the publicly available, anonymized PARROT v1.0 dataset
- No personal health information (PHI) is processed or stored
- Data processing aligns with GDPR Article 89 (scientific research)

**Data Sources**:
- [PARROT v1.0 Dataset](https://github.com/PARROT-reports/PARROT_v1.0) - Anonymized, multi-language radiology reports
- [Xt-EHR FHIR IG v0.2.1](https://www.xt-ehr.eu/fhir/models/) - Open-source model specifications

---

## 4. AI Literacy and Responsible Use

### 4.1 AI Literacy Requirements (Article 4)

**Project Team AI Literacy**:
- Understanding of AI capabilities and limitations
- Awareness of potential biases in language models
- Knowledge of transparency and accountability requirements
- Training on responsible AI use in healthcare contexts

**Stakeholder Communication**:
- Clear disclosure of AI involvement in all documentation
- Transparent methodology and validation processes
- Accessible explanations of AI-assisted analysis

### 4.2 Risk Mitigation Measures

**Quality Assurance**:
1. **Source Verification**: All references link to official repositories and authoritative sources
2. **Version Control**: Specific version tracking for all data sources and models
3. **Reproducibility**: Complete documentation of methodology and validation steps
4. **Traceability**: Direct mapping from findings to source elements
5. **Expert Review**: Human validation of all AI-generated classifications and recommendations

**Limitations and Disclaimers**:
- AI analysis is based on available data and may not capture all edge cases
- Recommendations are advisory and subject to implementation context
- Findings should be interpreted within the scope of the dataset analyzed

---

## 5. General-Purpose AI Model Considerations

### 5.1 GPAI Model Compliance

Claude Sonnet 4.5 is a **General-Purpose AI (GPAI) model** under the AI Act. The provider (Anthropic) is responsible for:

**GPAI Provider Obligations** (Article 53):
- Transparency requirements and documentation
- Copyright compliance in training data
- Technical documentation and capability assessment
- Risk management for systemic risks (if applicable)

**Our Use of GPAI**:
- We use Claude Sonnet 4.5 as a **deployer** for analysis purposes
- The AI model is not fine-tuned or modified
- Usage aligns with the provider's intended purpose and terms of service

### 5.2 Systemic Risk Assessment

Claude Sonnet 4.5, as a high-capability model, may be classified as having **systemic risk** under Article 51. However:

- This project uses the model for **research and analysis**, not for deployment in critical systems
- The AI does not autonomously make healthcare decisions
- All outputs are subject to human review and validation
- The project operates under controlled, non-critical conditions

---

## 6. Implementation Roadmap and AI Act Timeline

### 6.1 AI Act Application Timeline

The EU AI Act entered into force on **2 August 2024** with phased implementation:

| Date | Milestone | Project Impact |
|------|-----------|----------------|
| **2 February 2025** | Prohibited practices effective | ✅ Project does not involve prohibited AI practices |
| **2 August 2025** | GPAI model obligations | ✅ Using compliant GPAI provider (Anthropic) |
| **2 August 2026** | High-risk AI rules effective | ✅ Project classified as Limited Risk, not High-Risk |
| **2 August 2027** | Product-related high-risk rules | ℹ️ Not applicable (research/analysis project) |

### 6.2 Ongoing Compliance Measures

**Current Compliance Status**:
- ✅ Transparency requirements met through AI attribution
- ✅ AI-generated content clearly marked
- ✅ Human oversight and expert review established
- ✅ Documentation and traceability maintained

**Future Considerations**:
- Monitor updates to AI Act guidance and implementing acts
- Review GPAI Code of Practice when finalized
- Align with AI Office guidance for healthcare applications
- Update documentation as regulations evolve

---

## 7. References and Resources

### 7.1 EU AI Act Official Resources

| Resource | Link | Description |
|----------|------|-------------|
| **EU AI Act Full Text** | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Official legislation |
| **European Commission AI Act Hub** | [AI Act Overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) | Policy guidance and updates |
| **Irish Implementation** | [Enterprise Ireland AI Act](https://enterprise.gov.ie/en/what-we-do/innovation-research-development/artificial-intelligence/eu-ai-act/) | National guidance and timeline |
| **AI Act Service Desk** | [Single Information Platform](https://ai-act-service-desk.ec.europa.eu/en) | Interactive compliance tools |
| **European AI Office** | [AI Office Portal](https://digital-strategy.ec.europa.eu/en/policies/ai-office) | Governance and enforcement |

### 7.2 Healthcare and EHDS Resources

| Resource | Link | Description |
|----------|------|-------------|
| **European Health Data Space** | [EHDS Regulation](https://health.ec.europa.eu/ehealth-digital-health-and-care/european-health-data-space_en) | Healthcare data framework |
| **Xt-EHR Project** | [Official Site](https://www.xt-ehr.eu/) | EHDS model development |
| **GDPR** | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Data protection framework |

### 7.3 AI Governance and Ethics

| Resource | Link | Description |
|----------|------|-------------|
| **AI Continent Action Plan** | [Commission Plan](https://digital-strategy.ec.europa.eu/en/policies/ai-continent-action-plan) | EU AI strategy |
| **GPAI Code of Practice** | [Code Development](https://digital-strategy.ec.europa.eu/en/policies/ai-code-practice) | Industry compliance guidance |
| **Ethics Guidelines for Trustworthy AI** | [High-Level Expert Group](https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai) | Ethical AI principles |

---

## 8. Contact and Governance

### 8.1 Project Governance

**Responsible Team**: Xt-EHR T7.2 Sub-team for Imaging Reports Model  
**Project Oversight**: Xt-EHR Joint Action governance structure  
**Expert Review**: Healthcare informatics and interoperability specialists

### 8.2 Compliance Inquiries

For questions regarding EU AI Act compliance or AI usage in this project:

**Single Point of Contact**: 
- Ireland: [AIinfo@enterprise.gov.ie](mailto:AIinfo@enterprise.gov.ie)
- EU Commission: [AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/en)

**Project-Specific Inquiries**:
- Refer to Xt-EHR governance channels
- See project README.md for team contacts

---

## 9. Version History and Updates

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | November 2025 | Initial EU AI Act compliance document | Xt-EHR T7.2 Sub-team |

**Review Cycle**: This document will be reviewed quarterly and updated as needed to reflect:
- EU AI Act implementing acts and guidance
- GPAI Code of Practice developments
- AI Office recommendations
- Project scope or methodology changes

---

## Disclaimer

This document provides information for compliance purposes and does not constitute legal advice. Organizations implementing recommendations from this project should consult the EU AI Act directly and, when necessary, obtain professional legal guidance.

The AI Act is a complex regulation with ongoing development of implementing acts and guidance. Users should refer to official EU sources for the most current requirements and consult with qualified legal professionals for specific compliance needs.

---

**Document Classification**: Public  
**License**: Part of Xt-EHR T7.2 Sub-team analysis work  
**Last Review**: November 2025
