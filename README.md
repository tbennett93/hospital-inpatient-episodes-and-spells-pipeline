# Inpatient Episodes & Spells Data Pipeline (WIP)

## Purpose

Build an AWS-based data pipeline to transform **source-system inpatient episode data** into analytically useful **episode and spell fact tables**, with calculated measures and appropriately modelled dimensions.

The pipeline is designed to:
- Handle mutable episode records
- Preserve clinical semantics (episodes vs spells)
- Produce a clean relational model for downstream analytics

---

## High-Level Architecture

- **Storage:** Amazon S3  
- **Processing / Querying:** Amazon Athena  
- **Orchestration:** AWS Step Functions  
- **Compute:** AWS Lambda (boto3)  
- **Build Pattern:** Medallion (Bronze → Silver → Gold)

---

## Technology Choices

### Why Athena
- Serverless with minimal operational overhead
- Native integration with S3
- Strong support for CTAS and analytical SQL
- Well-suited for moderate-sized healthcare datasets

### Why Views
- Encapsulate complex transformation logic
- Reusable across CTAS operations
- Separate business logic from physical table creation
- Simplify CTAS operations within calling functions

### Why Drop-and-Rebuild
- Source system provides **snapshots**, not change logs
- Table sizes do not justify incremental complexity
- Rebuilds simplify correctness guarantees

---

## Data Model Overview

### Clinical Concepts
- Patients are admitted
- Admissions consist of one or more **episodes**
- Episodes may change while active - we always want to report the most recent version of the truth
- Once discharged, episode records are immutable
- A **spell** represents a continuous inpatient stay across episodes

---

## Medallion Layers

### Bronze

Raw ingestion layer.

- Append-only
- Source-system snapshot (1 row per episode)
- CSV → Parquet conversion
- Daily snapshot pushed by source system
- No business logic applied 
- No schema enforcement - this is pushed downstream to silver

**Purpose:** Preserve raw history and source fidelity.

---

### Silver

Cleaned, validated, and de-duplicated layer.

**Transformations:**
- One row per episode (latest version only)
- No in-episode historical tracking at this level
- Standardised column naming
- Trimmed whitespace
- Schema validation
  - Explicit date parsing
  - Fail hard on unexpected values

**Load Pattern:**
- Full rebuild daily
- Triggered via EventBridge (08:00)
- Incremental loading not justified by data volume

**Rationale:**  
Silver represents the **current truth** for each episode.

---

### Gold

Analytical fact and dimension tables.

#### Fact Tables

**Episodes**
- One row per episode
- Latest episode in spell flag
- Discharged flag
- Episode number within spell
- Represents most recent episode state

**Spells**
- One row per spell
- Derived from episode grouping
- Length of stay calculated from:
  - First episode start date
  - Last episode discharge date

---

#### Dimensions (SCD Type 1)

- **Ward**
- **Patient**
  - Age at episode start
  - Age at discharge
- **Consultant**

**Why SCD1 (not SCD2):**
- Silver already represents the most recent episode state
- Historical episode changes are not retained at silver
- SCD2 would add complexity without much analytical benefit

**Why Consultant is not a Dimension:**
- Source system only provides a consultant identifier
- No additional attributes available

---

## Orchestration

- Step Functions coordinate:
  - S3 cleanup
  - Athena CTAS execution
  - Dependency ordering
- Lambda functions are modularised for reuse
- Athena execution status is surfaced to Step Functions

---

## Current Limitations / TODO

- Add async waits for Athena where required
- Alert on empty source tables
- Allow pipeline continuation when no data found (graceful S3 cleanup)
- Improve Athena failure reporting in Step Functions
- Consider SCD2s
- Consider building into DW (reshift)

---

## Design Notes

- Gold layer is intentionally relational (facts + dimensions)
- Normalisation improves:
  - Reusability
  - Analytical clarity
  - Downstream BI modelling
- SCD1 dimensions can be derived entirely from Silver

---

## Dependencies

- `pandas`
- `boto3`
