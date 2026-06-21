# Tools Catalog for AI-Native Data Engineers

## Warehouses & Databases

| Tool | MCP Server | Best For |
|---|---|---|
| Snowflake | `mcp-snowflake` | Cloud-native analytics, multi-cloud |
| BigQuery | `mcp-bigquery` | GCP-native, ADK integration |
| Microsoft Fabric / Synapse | `skills-for-fabric` | Microsoft stack |
| PostgreSQL | `@modelcontextprotocol/server-postgres` | Open-source, self-hosted |
| DuckDB | `@modelcontextprotocol/server-sqlite` (compatible) | Local dev, embedded analytics |
| Databricks | Community MCP | Lakehouse, ML integration |
| Redshift | Community MCP | AWS-native |

---

## Transformation

| Tool | Claude Integration | Notes |
|---|---|---|
| dbt Core | Native — Claude generates models, tests, docs | Industry standard |
| dbt Cloud | Via dbt Core patterns | Managed dbt |
| SQLMesh | dbt-compatible syntax | Better CI/CD, virtual environments |
| Dataform | Native to Google ADK data-engineering agent | BigQuery-native |
| dlt (data load tool) | Python SDK — Claude generates pipelines | Great for ingestion agents |
| Spark / PySpark | Claude generates PySpark code | Big data processing |

---

## Orchestration

| Tool | Claude Integration | Notes |
|---|---|---|
| Airflow | Claude generates DAGs | Most widely used |
| Dagster | Asset-based model, Claude generates assets | Best alignment with data contracts |
| Prefect | Python-native, Claude generates flows | Developer-friendly |
| GitHub Actions | Native CI/CD for Claude Code headless | Pipeline CI/CD, review automation |
| Fabric Pipelines | Via `fabric-authoring` skill | Microsoft-native |
| Cloud Composer | Via Airflow patterns | GCP-managed Airflow |

---

## Data Quality

| Tool | Claude Integration | Notes |
|---|---|---|
| dbt tests | Native — Claude generates test YAML | Static quality checks |
| Great Expectations | MCP server available | Programmatic expectations |
| Soda | Claude generates Soda checks | Lightweight, SQL-based |
| Elementary | dbt-native anomaly detection | Production monitoring |
| Custom DQ Agents | See `data-engineering/02-data-quality-agent/` | Full AI-native DQ |

---

## Data Catalog & Lineage

| Tool | Claude Integration | Notes |
|---|---|---|
| dbt docs | Auto-generated from dbt models | Free, built-in |
| DataHub | MCP server for metadata | LinkedIn open-source |
| Atlan | Claude writes descriptions to Atlan | Enterprise catalog |
| OpenMetadata | Growing MCP support | Open-source |
| Alation | API integration | Enterprise |

---

## Infrastructure & DevOps

| Tool | Claude Integration | Notes |
|---|---|---|
| Terraform | Claude generates HCL | Cloud IaC |
| Pulumi | Python-first, Claude generates code | Developer-friendly IaC |
| Docker | Claude generates Dockerfiles | Container management |
| GitHub | `@modelcontextprotocol/server-github` | Code management, PR automation |
| GitHub Actions | Claude Code headless mode | CI/CD pipeline |

---

## Frameworks & Methods

| Framework | Purpose | Install |
|---|---|---|
| BMAD Method | Agile AI-driven development methodology | `github.com/bmad-code-org/BMAD-METHOD` |
| BMAD for Claude Code | BMAD skills as slash commands | `github.com/aj-geddes/claude-code-bmad-skills` |
| Superpowers | Full dev lifecycle framework | Anthropic marketplace |
| Google ADK | Open-source agent framework | `github.com/google/adk-python` |
| Anthropic Agent SDK | Multi-agent orchestration | `pip install anthropic` |
