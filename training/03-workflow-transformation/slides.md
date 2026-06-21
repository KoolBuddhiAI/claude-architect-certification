---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Your Job, Upgraded
## What your actual workflows look like with the right tools

*Module 03 · AI-Native Data Engineering*

---

# Remember those three answers you wrote down?

In Module 00 you wrote:
1. The most repetitive thing you do
2. The work you wish you had time for
3. The decision only you can make

Pull them out. This module is built around them.

We're not going to talk about abstract workflows. We're going to map **your** work — task by task — to what it looks like with agents in the picture.

This is where it gets personal.

Every common DE task maps to a new pattern. By the end of this module you will see your daily work differently.

---

# Map 1: ETL / ELT Pipeline Development

**Legacy way:**
```
1. Write Python/SQL extraction script
2. Write transformation logic
3. Test locally with sample data
4. Deploy to Airflow / dbt
5. Debug production failures manually
```

**AI-native way:**
```
1. Define data contract (you own this)
2. Orchestrate ingestion agent (fetch + dedup + normalize)
3. Orchestrate transformation agent (schema-enforced output)
4. Quality gate agent validates before promotion
5. Anomaly detection agent monitors production
```

**What changed**: You specify and review. Agents execute.

---

# Map 1: ETL — Before vs After

| Step | Legacy | AI-Native |
|---|---|---|
| Extract | Write pagination logic | Agent handles with fetch_page tool |
| Transform | Write column-by-column mapping | Agent generates from data contract |
| Validate | Manual spot-check | Quality gate agent: structured report |
| Load | Write INSERT / MERGE logic | Agent uses load_records with dedup |
| Monitor | Alert on job failure only | Anomaly agent monitors data, not just job |
| Document | Write manually (often skipped) | Agent generates from lineage |

**Time savings**: 60–80% on implementation. **Quality improvement**: systematic vs spot-check.

---

# Map 2: Data Quality Management

**Legacy way:**
```
1. Analyst reports data issue via email
2. Engineer investigates in SQL
3. Root cause found after hours/days
4. Hotfix applied
5. Hope it doesn't happen again
```

**AI-native way:**
```
1. Quality gate agent runs on every pipeline execution
2. Structured report: severity, affected records, recommendation
3. Critical failures block promotion automatically
4. Root cause analysis agent investigates anomalies
5. Quality contract updated to catch it next time
```

**What changed**: Reactive → proactive. Post-hoc → pre-promotion gate.

---

# Map 2: Data Quality — Tool Mapping

| DQ Task | Legacy Tool | AI-Native Approach |
|---|---|---|
| Null checks | Great Expectations / dbt tests | DQ agent + structured report |
| Outlier detection | Manual SQL | Statistical check tool (3σ) |
| Schema validation | CI/CD schema test | Schema evolution agent |
| Duplicate detection | Ad-hoc SQL | DQ agent check_duplicates tool |
| Enum validation | dbt accepted_values | DQ agent check_enum_values tool |
| Trend anomaly | Dashboard observation | Anomaly detection agent |

**Key**: DQ agents don't replace dbt tests. They complement them with AI-reasoning about *what to do* with issues, not just *whether* they exist.

---

# Map 3: Reporting & Analytics (Power BI / Fabric)

**Legacy way:**
```
1. Analyst submits report request
2. Engineer builds semantic model or dataset
3. Analyst creates visuals manually
4. Review cycles over days/weeks
5. Report deployed and immediately outdated
```

**AI-native way (Microsoft Fabric stack):**
```
1. Analyst describes report requirements in natural language
2. Claude (fabric-authoring skill) scaffolds semantic model
3. Claude (powerbi-authoring skill) creates report layout
4. Engineer reviews data model accuracy
5. Analyst iterates visuals with Claude in real-time
```

**What changed**: Engineer focuses on semantic model correctness. AI handles scaffolding.

---

# Map 3: Power BI Migration Reality Check

Microsoft Fabric Skills for Claude (`skills-for-fabric`) enables:

| What Claude Can Do | What Still Needs You |
|---|---|
| Create semantic models from schema | Validate business metric definitions |
| Author PBIR report layouts | Confirm stakeholder requirements |
| Write DAX measures | Verify DAX correctness for business logic |
| Publish reports to workspace | Approve publishing (governance) |
| Troubleshoot slow queries | Decide on solution tradeoffs |

**Power BI Q&A retires December 2026.** The migration path: Claude + Fabric MCP.

---

# Map 4: SQL for Analytics Requests

**Legacy way:**
```
1. Analyst sends Slack message: "can you get me X?"
2. Engineer manually writes SQL
3. Engineer runs SQL, shares results
4. Analyst asks follow-up
5. Engineer repeats
```

**AI-native way:**
```
1. Analyst uses text-to-SQL agent (self-serve)
2. Agent introspects live schema
3. Agent validates SQL before running
4. Agent returns structured results
5. Engineer reviews only the complex or high-stakes queries
```

**What changed**: Engineer moves from SQL writer to SQL reviewer and system builder.

---

# Map 4: Text-to-SQL — What Works and What Doesn't

| Works Well | Needs Human Review |
|---|---|
| Standard aggregations (SUM, COUNT, GROUP BY) | Business-specific metric definitions |
| Joins on foreign keys | Multi-step derived metrics |
| Date range filtering | Queries touching PII |
| Well-documented schemas | Queries involving financial reconciliation |
| Exploratory queries | Queries that will be used for reporting |

**Rule**: Self-serve for exploration. Human review for anything that stakeholders will rely on.

---

# Map 5: Schema Changes & Migrations

**Legacy way:**
```
1. Receive schema change request
2. Manually write ALTER TABLE statements
3. Test in dev environment
4. Write rollback plan (often not done)
5. Deploy in maintenance window
6. Manually update downstream code
```

**AI-native way:**
```
1. Schema evolution agent: diff V1 vs V2
2. Agent classifies: breaking / non-breaking
3. Agent generates: forward SQL + rollback SQL
4. Engineer reviews classification and SQL
5. Agent generates: downstream impact analysis
6. Standard PR + CI/CD promotion
```

**What changed**: Classification and generation automated. Human owns the decision to proceed.

---

# Map 6: Data Catalog & Documentation

**Legacy way:**
- Documentation written manually and immediately outdated
- Data catalog populated when someone gets around to it
- Lineage tracked in a spreadsheet (or not at all)
- Column descriptions written by engineers who wrote the code years ago

**AI-native way:**
- Lineage generated automatically from BMAD architecture documents
- Column descriptions generated from context + schema + data samples
- Data catalog auto-populated by agents after each deployment
- Documentation reviewed by engineer, not written from scratch

**What changed**: Documentation becomes a review task, not a writing task.

---

# Your Workflow Transformation Map

Use this template for your own role:

```
Task: [Name a task you do regularly]

Legacy workflow:
1.
2.
3.

AI-native workflow:
1.
2.
3.

What I still own:
-
-

What agents handle:
-
-

Quality gate I need:
-
```

Complete this for your top 5 tasks from the Module 00 reflection exercise.

---

# Module 03 — Key Takeaways

- Every major DE workflow has a clear AI-native mapping
- The pattern is always: **you design + review, agents execute**
- Quality gates replace spot-check trust
- Power BI/Fabric teams have official Claude skill bundles available now
- Text-to-SQL is self-serve for exploration; human review for reporting
- Documentation shifts from writing to reviewing

**Next: Module 04 — Open Stack Guide**
