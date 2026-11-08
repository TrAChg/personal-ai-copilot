# PySpark Optimization, Kimball Star Schema (SCD Type 2), dbt and Unity Catalog Governance (Module 07 & NF26)

**Category**: `data_engineering` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

Data Engineering & Warehouse Core (AI/Module_07 and Project/NF26_Smart_Teems): (1) PySpark Tuning: Minimize Wide Transformations (Shuffle); use Broadcast Hash Join (broadcast(small_df)) when dimension table <100MB; resolve Data Skew via key salting or Adaptive Query Execution (AQE); optimize Delta Lake via OPTIMIZE + ZORDER BY on high-cardinality filter columns and VACUUM. (2) Data Modeling (Kimball Star Schema & dbt): Central Fact tables (granular measurements + foreign keys) surrounded by Dimension tables with SCD Type 2 (valid_from, valid_to, is_current) for historical tracking, built via modular dbt SQL layers (staging -> intermediate -> marts) and served to PowerBI. (3) Unity Catalog Governance: 3-level namespace (catalog.schema.table), Row-Level Security (RLS), Column Masking, and end-to-end lineage.

## Connected GraphRAG Entities

- `Databricks_Medallion_Lakehouse`
- `dbt_StarSchema_UnityCatalog`
