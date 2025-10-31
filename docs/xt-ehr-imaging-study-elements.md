# Xt-EHR Imaging Study Data Elements Analysis

**Source Model**: [EHDSImagingStudy v0.2.1](https://github.com/xt-ehr/xt-ehr-common/tree/main/input/fsh/EHDS-models/imagingStudy.fsh)  
**Analysis Date**: October 2025  
**Model Version**: Xt-EHR FHIR IG v0.2.1 (October 10, 2025)

## Model Overview

The Xt-EHR Imaging Study model (`EHDSImagingStudy`) provides the structure for DICOM study metadata and organization within imaging reports. This model facilitates location of available images and organizes information according to the established imaging study framework.

### Model Reference
```fsh
Logical: EHDSImagingStudy
Parent: EHDSDataSet
Title: "Imaging study model"
Description: """Imaging study model includes the key information about the content 
of an imaging study. It does not include image pixels but includes location pointers 
to its image content and organises this information according to the well-established 
model of an imaging study made of one or more series and each series made of instances 
or images. Composed of a set of data (DICOM KOS) that facilitates the location of 
all available images."""
```

**Source**: [imagingStudy.fsh](https://github.com/xt-ehr/xt-ehr-common/tree/main/input/fsh/EHDS-models/imagingStudy.fsh)

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
| **Identifier** | `header.identifier` | 1..* | Base | Identifier | DICOM Study Instance UID and other identifiers |
| **Authorship** | `header.authorship` | 1..* | Base | Base | Resource authoring details |
| **Author** | `header.authorship.author[x]` | 1..1 | Base | Choice | Author(s) who created the resource |
| **Authoring DateTime** | `header.authorship.datetime` | 1..1 | Base | dateTime | Date and time of authoring/issuing |
| **Status** | `header.status` | 1..1 | Base | CodeableConcept | Status of the resource or document |

### Optional Header Elements (Base)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Last Update** | `header.lastUpdate` | 0..1 | Base | dateTime | Date and time of the last update |
| **Status Reason** | `header.statusReason[x]` | 0..1 | Base | Choice | Reason for the current status |
| **Language** | `header.language` | 0..1 | Base | CodeableConcept | Language in which the resource is written |

---

## Study Level Elements

### Core Study Information (Base)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Modality** | `modality` | 0..* | Base | CodeableConcept | All distinct values for series modalities |
| **Encounter** | `encounter` | 0..1 | Base | EHDSEncounter | Associated encounter reference |
| **Started** | `started` | 0..1 | Base | dateTime | Date and time the study started |
| **Based On** | `basedOn` | 0..* | Base | EHDSServiceRequest | Diagnostic requests that resulted in this study |
| **Number of Series** | `numberOfSeries` | 0..1 | Base | integer | Number of Series in the Study |
| **Number of Instances** | `numberOfInstances` | 0..1 | Base | integer | Number of SOP Instances in Study |
| **Description** | `description` | 0..1 | Base | string | Institution-generated description of the study |
| **Study Custodian** | `studyCustodian` | 0..1 | Base | EHDSOrganisation | Organisation information |
| **Study Endpoint** | `studyEndpoint` | 0..1 | Base | EHDSEndpoint | Technical details for study access |

---

## Series Level Elements (Optional: 0..*)

### Core Series Information (Base)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Series UID** | `series.seriesUid` | 1..1 | Base | Identifier | DICOM Series Instance UID |
| **Acquisition Modality** | `series.acquisitionModality` | 1..1 | Base | CodeableConcept | Modality used for this series |
| **Number** | `series.number` | 0..1 | Base | integer | Numeric identifier of this series |
| **Description** | `series.description` | 0..1 | Base | string | Human readable summary of the series |
| **Number of Instances** | `series.numberOfInstances` | 0..1 | Base | integer | Number of Series Related Instances |
| **Series Endpoint** | `series.seriesEndpoint` | 0..1 | Base | EHDSEndpoint | Technical details for series access |
| **Body Site** | `series.bodySite` | 0..1 | Base | EHDSBodyStructure | Body part (with laterality) examined |
| **Specimen** | `series.specimen` | 0..* | Base | EHDSSpecimen | Specimen imaged |
| **Started** | `series.started` | 0..1 | Base | dateTime | When the series started |

---

## Instance Level Elements (Optional: 0..*)

### Core Instance Information (Base)

| Element | Path | Cardinality | Status | Type | Description |
|---------|------|-------------|--------|------|-------------|
| **Instance UID** | `series.instancesInTheSeries.instanceUid` | 1..1 | Base | Identifier | DICOM SOP Instance UID |
| **SOP Class** | `series.instancesInTheSeries.sopClass` | 1..1 | Base | uri | DICOM class type |
| **Instance Title** | `series.instancesInTheSeries.instanceTitle` | 0..1 | Base | string | Description of the instance |
| **Instance Number** | `series.instancesInTheSeries.instanceNumber` | 0..1 | Base | integer | Number of this instance in the series |
| **Number of Frames** | `series.instancesInTheSeries.numberOfFrames` | 0..1 | Base | integer | Number of frames in multiframe instance |

---

## Element Categories by Usage Level

### Always Required Elements (6 elements)
1. **header.subject** (1..1) - Patient information
2. **header.identifier** (1..*) - Study identifiers including DICOM UID
3. **header.authorship** (1..*) - Authoring details
4. **header.authorship.author[x]** (1..1) - Author information
5. **header.authorship.datetime** (1..1) - Authoring timestamp
6. **header.status** (1..1) - Resource status

### Conditionally Required Elements (2 elements)
1. **series.seriesUid** (1..1) - Required if series present
2. **series.acquisitionModality** (1..1) - Required if series present
3. **series.instancesInTheSeries.instanceUid** (1..1) - Required if instance present
4. **series.instancesInTheSeries.sopClass** (1..1) - Required if instance present

### Optional Study-Level Elements (9 elements)
1. **header.lastUpdate** (0..1)
2. **header.statusReason[x]** (0..1)
3. **header.language** (0..1)
4. **modality** (0..*)
5. **encounter** (0..1)
6. **started** (0..1)
7. **basedOn** (0..*)
8. **numberOfSeries** (0..1)
9. **numberOfInstances** (0..1)
10. **description** (0..1)
11. **studyCustodian** (0..1)
12. **studyEndpoint** (0..1)

### Optional Series-Level Elements (7 elements)
1. **series.number** (0..1)
2. **series.description** (0..1)
3. **series.numberOfInstances** (0..1)
4. **series.seriesEndpoint** (0..1)
5. **series.bodySite** (0..1)
6. **series.specimen** (0..*)
7. **series.started** (0..1)

### Optional Instance-Level Elements (3 elements)
1. **series.instancesInTheSeries.instanceTitle** (0..1)
2. **series.instancesInTheSeries.instanceNumber** (0..1)
3. **series.instancesInTheSeries.numberOfFrames** (0..1)

---

## Summary Statistics

### Required Elements: 6-10 elements
- **Always Required**: 6 elements
- **Conditionally Required**: 4 elements (when hierarchical levels are present)

### Optional Elements: 21 elements
- **Study Level Optional**: 12 elements
- **Series Level Optional**: 6 elements  
- **Instance Level Optional**: 3 elements

### Total Base Elements: ~27 elements

---

## Usage Characteristics

### Technical/Metadata Elements (High Priority)
- Study, Series, and Instance UIDs
- Modality information
- Timestamps
- Patient identification
- Status information

### Administrative Elements (Medium Priority)
- Encounter references
- Service requests
- Organization information
- Endpoints for data access

### Descriptive Elements (Lower Priority)
- Descriptions and titles
- Numbers and counts
- Additional metadata

### Clinical Context Elements (Variable Priority)
- Body site information
- Specimen details
- Clinical associations

---

## Notes
- The model follows DICOM hierarchy: Study → Series → Instance
- Required elements focus on core identification and technical metadata
- Many optional elements provide enhanced metadata for interoperability
- DICOM UIDs are critical for technical implementation
- Series and Instance levels may be completely absent in summary use cases
- Model is more technical/metadata-focused compared to the clinical focus of ImagingReport