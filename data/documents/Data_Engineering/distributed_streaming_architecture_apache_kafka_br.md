# Distributed Streaming Architecture: Apache Kafka Brokers, Partitions, Consumer Groups and Exactly-Once (Module 06)

**Category**: `data_engineering` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

Event-Driven Streaming (AI/Module_06): Choose Apache Kafka over REST/RabbitMQ for high-throughput, durable, replayable event logs and Change Data Capture (CDC). Core mechanics: (1) Topics are sharded into Partitions (the unit of parallelism); strict ordering is guaranteed ONLY within a single partition via hash(message_key) mod P. (2) Durability and Fault Tolerance: Leader + Follower replicas across Brokers with acks=all and min.insync.replicas=2. (3) Consumer Groups: Horizontal scaling where each partition is consumed by at most ONE consumer within a group (avoid having more consumers than partitions). (4) Delivery Semantics: At-Least-Once (commit offset after processing + idempotent sink) vs. Exactly-Once (transactional producer + read_committed).

## Connected GraphRAG Entities

- `Databricks_Medallion_Lakehouse`
- `Apache_Kafka_Streaming`
