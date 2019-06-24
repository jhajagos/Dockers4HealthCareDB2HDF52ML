# Dockers and scripts for mapping data to OHDSI and to HDF5 file formats for machine learning

## Build docker images


### Upload Athena generated vocabulary to S3

Due to copyright issues with medical vocabularies the process of vocabulary building requires manual intervention. For the
automated docker build process we need to upload the vocabulary to an S3 bucket. The s3 bucket is based on unique hash for
the zip file.

http://athena.ohdsi.org/vocabulary/list

Select the vocabularies that you want to to include. For most modern EHR systems you will want: SNOMED, CPT4, HCPCS,
LOINC, RxNorm, NDC, Gender, Race, CMS Place of Service, ATC, Revenue Codes, Ethnicity, NUCC, SPL, ICD10CM, ICDCM, and ICD9Proc.

### Upload RxNorm to S3

