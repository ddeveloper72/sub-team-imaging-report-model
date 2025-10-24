# Xt-EHR Imaging Report Data Elements Analysis

## Model: EHDSImagingReport

Based on the structure definition from: https://build.fhir.org/ig/Xt-EHR/xt-ehr-common/StructureDefinition-EHDSImagingReport.html

### Legend
- **Cardinality**: 
  - `1..1` = Required (exactly one)
  - `1..*` = Required (one or more)
  - `0..1` = Optional (zero or one)
  - `0..*` = Optional (zero or more)
- **Base Elements**: Elements with Status="Base" (fundamental to the model)

---

## Header Section (Required: 1..1)

### Core Header Elements (Base)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Subject** | `header.subject` | 1..1 | Base | EHDSPatient | Patient/subject information |
| **Identifier** | `header.identifier` | 1..* | Base | Identifier | Unique identifier of the document |
| **Authorship** | `header.authorship` | 1..* | Base | Base | Report authoring details |
| **Author** | `header.authorship.author[x]` | 1..1 | Base | Choice | Author by whom the document was authored |
| **Authoring DateTime** | `header.authorship.datetime` | 1..1 | Base | dateTime | Date and time of authoring/issuing |
| **Status** | `header.status` | 1..1 | Base | CodeableConcept | Status of the document |
| **Document Type** | `header.documentType` | 1..1 | Base | CodeableConcept | Type of document (medical imaging report) |
| **Document Title** | `header.documentTitle` | 1..1 | Base | string | Human readable document title |

### Optional Header Elements (Base)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Last Update** | `header.lastUpdate` | 0..1 | Base | dateTime | Date and time of the last update |
| **Status Reason** | `header.statusReason[x]` | 0..1 | Base | Choice | Reason for the current status |
| **Language** | `header.language` | 0..1 | Base | CodeableConcept | Language in which the resource is written |
| **Period** | `header.period` | 0..1 | Base | Period | Time of service being documented |
| **Version** | `header.version` | 0..1 | Base | string | Business version of the document |
| **Attestation** | `header.attestation` | 0..* | Base | Base | Document attestation details |
| **Legal Authentication** | `header.legalAuthentication` | 0..1 | Base | Base | Document legal authentication details |
| **Event Type** | `header.eventType` | 0..* | Base | CodeableConcept | Categorisation of the event covered |
| **Service Specialty** | `header.serviceSpecialty` | 0..* | Base | CodeableConcept | Clinical specialty details |
| **Custodian** | `header.custodian` | 0..1 | Base | EHDSOrganisation | Organisation maintaining the document |
| **Confidentiality** | `header.confidentiality` | 0..1 | Base | CodeableConcept | Level of confidentiality |
| **Accession Number** | `header.accessionNumber` | 0..1 | Base | string | RIS identifier for the imaging procedure |
| **Health Insurance Info** | `header.healthInsuranceAndPaymentInformation` | 0..* | Base | EHDSCoverage | Health insurance and payment information |
| **Intended Recipient** | `header.intendedRecipient[x]` | 0..* | Base | Choice | Information recipient |

---

## Body Section (Optional: 0..1)

### Order Information (Optional: 0..*)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Order ID** | `body.orderInformation.orderId` | 1..* | Base | Identifier | Identifier(s) of the imaging service order |
| **Order Date Time** | `body.orderInformation.orderDateAndTime` | 0..1 | Base | dateTime | Date and time of the order placement |
| **Order Placer** | `body.orderInformation.orderPlacer[x]` | 0..1 | Base | Choice | Person/organisation placing the order |
| **Order Reason Text** | `body.orderInformation.orderReasonText` | 0..* | Base | string | Textual explanation for the service request |
| **Order Reason** | `body.orderInformation.orderReason[x]` | 0..* | Base | Choice | Coded explanation for the service request |
| **Clinical Question** | `body.orderInformation.clinicalQuestion` | 0..1 | Base | string | Clinical question to be answered |

### Supporting Information (Optional: 0..1)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Observation** | `body.supportingInformation.observation` | 0..* | Base | EHDSObservation | Clinical findings and observations |
| **Condition** | `body.supportingInformation.condition` | 0..* | Base | EHDSCondition | Conditions affecting service/interpretation |
| **Medication Administration** | `body.supportingInformation.medicationAdministration` | 0..* | Base | EHDSMedicationAdministration | Medications for the procedure |
| **Devices** | `body.supportingInformation.devices` | 0..* | Base | EHDSDevice | Implants/devices affecting examination |
| **Pregnancy Status** | `body.supportingInformation.pregnancyStatus` | 0..1 | Base | EHDSCurrentPregnancy | Pregnancy status during examination |
| **Sex for Clinical Use** | `body.supportingInformation.sexForClinicalUse` | 0..* | Base | CodeableConcept | Sex parameter for clinical decision making |
| **Other Supporting Info** | `body.supportingInformation.otherSupportingInformation` | 0..* | Base | Resource | Any other relevant supporting information |

### Specimen Information (Optional: 0..*)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Specimen** | `body.specimen` | 0..* | Base | EHDSSpecimen | Specimen information |

### Service Request (Optional: 0..*)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Service Request** | `body.serviceRequest` | 0..* | Base | EHDSServiceRequest | Specification of requested service(s) |

### Exposure Information (Optional: 0..1)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Effective Dose** | `body.exposureInformation.effectiveDose` | 0..* | Base | Quantity | Effective dose in mSv |
| **Equivalent Dose Info** | `body.exposureInformation.equivalentDoseInformation` | 1..1 | Base | Base | Equivalent dose information |
| **Equivalent Dose** | `body.exposureInformation.equivalentDoseInformation.equivalentDose` | 1..1 | Base | Quantity | Equivalent dose in mSv |
| **Tissue Type** | `body.exposureInformation.equivalentDoseInformation.tissueType` | 1..1 | Base | CodeableConcept | Type of tissue for dosage enumeration |

---

## Examination Report Section (Required if body present: 1..1)

### Core Examination Elements

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Modality** | `body.examinationReport.modality` | 1..* | Base | CodeableConcept | Imaging modality used |
| **Body Part** | `body.examinationReport.bodyPart` | 0..* | Base | EHDSBodyStructure | All body parts investigated |
| **Imaging Procedures** | `body.examinationReport.imagingProcedures` | 0..* | Base | EHDSProcedure | Imaging procedures performed |
| **Medication** | `body.examinationReport.medication` | 0..* | Base | EHDSMedicationAdministration | Medication administered (contrast, etc.) |
| **Adverse Reaction** | `body.examinationReport.adverseReaction` | 0..* | Base | EHDSAllergyIntolerance | Adverse reactions during investigation |

### Result Data (Optional: 0..1)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Result Text** | `body.examinationReport.resultData.resultText` | 1..1 | Base | string | Narrative representation of results |
| **Observation Results** | `body.examinationReport.resultData.observationResults` | 0..* | Base | EHDSObservation | Detailed observation results |

### Conclusion (Required if examination report present: 1..1)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Impression** | `body.examinationReport.conclusion.impression` | 1..1 | Base | string | Narrative clinical conclusion |
| **Condition or Finding** | `body.examinationReport.conclusion.conditionOrFinding[x]` | 0..* | Base | Choice | Structured findings from investigation |

### Recommendation (Optional: 0..1)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Description** | `body.recommendation.description` | 1..1 | Base | string | Narrative description of recommendations |
| **Care Plan** | `body.recommendation.carePlan` | 0..* | Base | EHDSCarePlan | Structured care plan information |

### Comparison Study (Optional: 0..*)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Comparison Study** | `body.comparisonStudy` | 0..* | Base | EHDSImagingReport | Reference to prior imaging reports |

---

## Additional Sections

### DICOM Study Metadata (Optional: 0..*)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **DICOM Study Metadata** | `dicomStudyMetadata` | 0..* | Base | EHDSImagingStudy | Metadata of the DICOM study |

### Attachments (Optional: 0..*)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Attachments** | `attachments[x]` | 0..* | Base | Choice | Report attachments |

### Presented Form (Optional: 0..*)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Presented Form** | `presentedForm` | 0..* | Base | EHDSAttachment | PDF version or narrative representation |

---

## Summary Statistics

### Required Elements (Base Status)
- **Always Required (1..1 or 1..*)**: 8 elements
- **Conditionally Required**: 4 elements (when parent is present)

### Optional Elements (Base Status)  
- **Header Optional**: 11 elements
- **Body Optional**: 25+ elements
- **Total Optional**: 35+ elements

### Total Base Elements: ~47 elements

---

## Notes
- All elements listed have "Base" status in the terminology bindings
- Choice elements (indicated by [x]) can have multiple type options
- Complex elements contain sub-elements that expand the total count
- Many optional elements are designed for comprehensive clinical documentation
- Required elements focus on core identification, authorship, and clinical findings