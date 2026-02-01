# Inpatient Episodes & Spells Data Pipeline (WIP)

## Purpose

Build an AWS-based data pipeline to transform **source-system inpatient episode data** into analytically useful **episode and spell fact tables**, with calculated measures and appropriately modelled dimensions.

The pipeline is designed to:
- Handle mutable episode records
- Preserve clinical semantics (episodes vs spells)
- Produce a clean, relational model for downstream analytics
- Execute deterministically with synchronous orchestration

---

## High-Level Architecture

- **Storage:** Amazon S3  
- **Query Engine:** Amazon Athena  
- **Orchestration:** AWS Step Functions  
- **Compute / Glue Logic:** AWS Lambda (boto3)  
- **Build Pattern:** Medallion (Bronze → Silver → Gold)

---

## Technology Choices

### Why Athena
- Serverless with minimal operational overhead
- Native integration with S3
- Strong support for CTAS-based table builds
- Well-suited for moderate-sized healthcare datasets

### Why SQL-in-S3
- Transformation logic stored as versioned `.sql` files in S3
- Step Functions dynamically pull SQL text at runtime
- Keeps orchestration separate from business logic
- Enables reuse across Silver and Gold pipelines

### Why Drop-and-Rebuild
- Source system provides **snapshots**, not change logs
- Table sizes do not justify incremental complexity
- Rebuilds provide strong correctness guarantees
- Enables deterministic, idempotent runs

---

## Data Model Overview

### Clinical Concepts
- Patients are admitted
- Admissions consist of one or more **episodes**
- Episodes may change while active
- Once discharged, episode records are immutable
- A **spell** represents a continuous inpatient stay across episodes

---

## Medallion Layers

### Bronze

Raw ingestion layer.

- Append-only
- Source-system daily snapshot (1 row per episode)
- CSV → Parquet conversion
- No business logic applied
- No schema enforcement (deferred to Silver)

**Purpose:** Preserve raw history and source fidelity.

---

### Silver

Cleaned, validated, and de-duplicated layer representing the **current truth**.

**Transformations:**
- One row per episode (latest version only)
- No intra-episode historical tracking
- Standardised column naming
- Trimmed whitespace
- Schema validation:
  - Explicit date parsing
  - Fail-fast on unexpected values

**Load Pattern:**
- Full rebuild
- Triggered daily via EventBridge
- Synchronous Athena execution via Step Functions
- Drop + CTAS executed in a single Athena query per dataset

**Rationale:**  
Silver represents the authoritative, most recent state of each episode.

---

### Gold

Analytical fact and dimension tables.

#### Fact Tables

**Episodes**
- One row per episode
- Latest-episode-in-spell flag
- Discharged flag
- Episode number within spell

**Spells**
- One row per spell
- Derived from episode grouping
- Length of stay calculated from:
  - First episode start date
  - Final episode discharge date

---

#### Dimensions (SCD Type 1)

- **Ward**
- **Patient**
  - Age at episode start
  - Age at discharge
- **Consultant**

**Why SCD1 (not SCD2):**
- Silver already represents the most recent episode state
- Historical episode changes are not retained at Silver
- SCD2 would add complexity without analytical benefit

**Why Consultant is limited:**
- Source system provides only a consultant identifier
- No additional descriptive attributes available

---

## Orchestration

- EventBridge triggers the daily pipeline
- Step Functions orchestrate:
  - Bronze → Silver → Gold dependency ordering
  - Synchronous Athena query execution
  - Parallel execution of independent Gold pipelines
- SQL is retrieved from S3 at runtime
- Lambda functions are modularised and reused across layers
- Athena execution status is surfaced directly to Step Functions

---

## Current Limitations / TODO

- Alert on empty or missing source snapshots
- Graceful handling when no new data is present
- Improve Athena error reporting and failure context
- Add monitoring and alerting (CloudWatch)
- Evaluate SCD2 support if analytical needs evolve
- Consider migrating Gold layer into Redshift

---

## Design Notes

- Gold layer is intentionally relational (facts + dimensions)
- Normalisation improves:
  - Reusability
  - Analytical clarity
  - Downstream BI modelling
- SCD1 dimensions can be fully derived from Silver

---

## Dependencies

- `boto3`
- `pandas`
