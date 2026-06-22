---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# "Do I need to rip out my whole stack?"

*No. Here's what actually needs to change.*

*Module 04 · AI-Native Data Engineering*

---

# The answer most people want

> "I already use Snowflake / Fabric / BigQuery / Postgres. Do I have to change everything?"

No. You don't.

The patterns you learned in Modules 02 and 03 work on your existing stack. What changes is how you **connect** Claude to your systems — and a few tool choices that make the connection smoother.

This module is practical: here's what to keep, what to add, and why.

---

# The Stack Philosophy

> "Be opinionated about patterns. Be open about platforms."

The agent patterns you've learned work the same whether your warehouse is:
- Snowflake, BigQuery, Fabric, Postgres, Redshift, DuckDB

The **patterns** are portable. The **MCP servers** swap out.

This module helps you choose tools that maximize value and minimize total cost of ownership (TCO).

---

# TCO: The Full Picture

Most teams calculate tool cost as:
```
TCO = License cost
```

AI-native TCO is:
```
TCO = License + Engineer time + Maintenance + Context-switching
      − Agent-accelerated throughput savings
      − Quality-prevented incident costs
      − Self-serve analytics deflection
```

Tools that work well with Claude reduce the right side significantly.

---

# Data Warehouse — Recommendations

| Warehouse | Claude Compatibility | Notes |
|---|---|---|
| **Snowflake** | ⭐⭐⭐⭐⭐ | Native MCP server, dbt, great schema introspection |
| **BigQuery** | ⭐⭐⭐⭐⭐ | ADK native, BigQuery MCP, Dataform integration |
| **Microsoft Fabric** | ⭐⭐⭐⭐⭐ | Official `skills-for-fabric` bundle |
| **Postgres** | ⭐⭐⭐⭐⭐ | `@modelcontextprotocol/server-postgres` |
| **DuckDB** | ⭐⭐⭐⭐ | Lightweight, great for local development and testing |
| **Redshift** | ⭐⭐⭐ | Works but fewer purpose-built MCP tools |
| **Databricks** | ⭐⭐⭐ | SQL MCP available, Delta Lake support |

**Pick what your team already knows. The MCP server makes it Claude-compatible.**

---

# Transformation Layer — Recommendations

| Tool | Claude Compatibility | Notes |
|---|---|---|
| **dbt** | ⭐⭐⭐⭐⭐ | Claude generates dbt models, tests, docs natively |
| **SQLMesh** | ⭐⭐⭐⭐ | dbt-compatible, better CI/CD story |
| **Dataform** | ⭐⭐⭐⭐⭐ | Native to Google ADK data engineering agent |
| **dlt** | ⭐⭐⭐⭐ | Python-first, great for ingestion agents |
| **Airbyte** | ⭐⭐⭐ | MCP server available for connector management |

**Recommendation**: dbt for most teams. Claude can generate, test, and document models.

---

# Orchestration — Recommendations

| Tool | Claude Compatibility | Notes |
|---|---|---|
| **Airflow** | ⭐⭐⭐⭐ | Claude generates DAGs; MCP available |
| **Prefect** | ⭐⭐⭐⭐ | Python-native, easier agent integration |
| **Dagster** | ⭐⭐⭐⭐⭐ | Asset-based model aligns with data contracts |
| **GitHub Actions** | ⭐⭐⭐⭐⭐ | Native CI/CD for headless Claude Code pipelines |
| **Fabric Pipelines** | ⭐⭐⭐⭐⭐ | Via `fabric-authoring` skill |

**Recommendation**: Dagster for new builds (asset model matches data contract thinking). GitHub Actions for CI/CD gates.

---

# Data Quality — Recommendations

| Tool | Claude Compatibility | Notes |
|---|---|---|
| **dbt tests** | ⭐⭐⭐⭐⭐ | Claude generates not_null, unique, accepted_values |
| **Great Expectations** | ⭐⭐⭐⭐ | MCP integration available |
| **Soda** | ⭐⭐⭐⭐ | Claude generates Soda checks from data contracts |
| **Elementary** | ⭐⭐⭐⭐ | dbt-native anomaly detection |
| **Custom DQ agents** | ⭐⭐⭐⭐⭐ | See `data-engineering/02-data-quality-agent/` |

**Recommendation**: dbt tests for static checks + custom DQ agent for dynamic/contextual checks. Don't replace one with the other.

---

# Catalog & Lineage — Recommendations

| Tool | Claude Compatibility | Notes |
|---|---|---|
| **DataHub** | ⭐⭐⭐⭐ | MCP server for metadata operations |
| **Atlan** | ⭐⭐⭐⭐ | Claude writes column descriptions to Atlan |
| **dbt docs** | ⭐⭐⭐⭐⭐ | Auto-generated from agent-written dbt models |
| **OpenMetadata** | ⭐⭐⭐ | Open-source, growing MCP support |

**Recommendation**: dbt docs as baseline (free, automatic). DataHub or Atlan for enterprise catalog needs.

---

# Compute & Infrastructure

| Tool | Claude Compatibility | Notes |
|---|---|---|
| **Terraform** | ⭐⭐⭐⭐⭐ | Claude generates HCL from architecture specs |
| **Pulumi** | ⭐⭐⭐⭐⭐ | Python-first IaC, agent-friendly |
| **Docker** | ⭐⭐⭐⭐⭐ | Claude generates Dockerfiles and compose configs |
| **GitHub Actions** | ⭐⭐⭐⭐⭐ | CI/CD for every pipeline stage |

**Recommendation**: Terraform for cloud infra. Docker + GitHub Actions for pipeline CI/CD.

---

# MCP Server Reference

```bash
# Databases
npx -y @modelcontextprotocol/server-postgres
npx -y @modelcontextprotocol/server-sqlite
npx -y mcp-snowflake

# Code & Project Management
npx -y @modelcontextprotocol/server-github
npx -y @modelcontextprotocol/server-filesystem

# Microsoft Fabric (official)
# Install via: skills-for-fabric repo → .claude-plugin auto-discovery

# Monitoring
npx -y @modelcontextprotocol/server-sentry

# Documentation
npx -y @modelcontextprotocol/server-fetch  # web research
```

**Security rule**: Scope every MCP server to the minimum access needed. Read-only for analytics; write for pipeline management only.

---

# TCO Example: Power BI Team Migration

**Before (legacy)**:
| Cost | Annual |
|---|---|
| Power BI Premium license | $20/user/month |
| Engineer time (report requests) | 2 hrs/week × 50 weeks |
| Analyst time (waiting for reports) | 3 hrs/week × 50 weeks |

**After (Claude + Fabric)**:
| Cost | Annual |
|---|---|
| Claude API + Fabric license | $30/user/month |
| Engineer time (architecture review only) | 30 min/week × 50 weeks |
| Analyst time (self-serve with Claude) | 1 hr/week × 50 weeks |

**Result**: 75% reduction in engineer report-request time. Analysts self-serve 70% of requests.

---

# Stack Decision Framework

For any tool decision, ask:

1. **Is there an MCP server?** (connectivity)
2. **Is there a Claude Code skill?** (methodology)
3. **Can Claude generate the config/code?** (implementation)
4. **Can Claude debug errors from it?** (operations)
5. **Does it have structured output / schema?** (agent-friendly)

Tools that score 5/5 have the lowest AI-native TCO.

---

# Module 04 — Key Takeaways

- Platform choice matters less than MCP + skill availability
- dbt + Dagster + GitHub Actions is the most agent-compatible open stack
- Microsoft Fabric has official Claude skills (use them for Fabric teams)
- TCO calculation must include agent-accelerated throughput savings
- Every tool decision: ask "does this have an MCP server and skill?"

**Next: Module 05 — Enterprise Patterns**
