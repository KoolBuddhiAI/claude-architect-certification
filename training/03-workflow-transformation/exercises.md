# Module 03: Hands-On Exercises

## Exercise 1 — Quick (20 min): Your Workflow Transformation Map

**Goal:** Make the module personal by mapping your actual work.

Pull out your Module 00 reflection answers. For each of your three answers, fill in:

**Task 1 (Most Repetitive):**
```
What it is:
How long it takes now:
AI-native version (what you'd do differently):
What you'd still own:
Quality gate you'd need:
Estimated time in AI-native version:
```

**Task 2 (Work you wish you had time for):**
```
What's blocking it:
Which repetitive tasks need to be transformed first:
How you'd spend the reclaimed time:
```

**Task 3 (Decision only you can make):**
```
What context makes it yours:
How the AI-native workflow gives you more time for this:
```

This is a 20-minute exercise that produces a document you can share with your manager.

---

## Exercise 2 — Medium (45 min): Run the Data Quality Agent

**Goal:** Experience the DQ agent from `data-engineering/02-data-quality-agent/` on your own data.

**Steps:**

1. Install requirements:
```bash
cd data-engineering
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
```

2. Run the sample to understand the output:
```bash
python 02-data-quality-agent/main.py
```

3. **Adapt it to your data:** Replace `DATASET` in `main.py` with a sample from a real table you work with (10–20 rows is enough). Update the `check_enum_values` calls to match your actual enums.

4. **Review the report:** Look at `overall_score`, the issues list, and the recommendations. Ask yourself:
   - Would this have caught the last data quality issue you dealt with?
   - What critical gate is missing?
   - What would you add to the quality contract?

**Reflection question:** The DQ agent surfaces issues programmatically. But deciding what severity level to assign each issue type — that's your judgment. What would you classify differently than the agent did?

---

## Exercise 3 — Deep (90 min): Build Your Personal Workflow Map and Pitch It

**Goal:** Produce a document that could convince your team to adopt one AI-native workflow.

**Part 1 — Choose your target workflow (10 min)**

Pick the one workflow from your map that:
- Has the highest time savings potential
- Has a concrete, reviewable quality gate
- You could implement within two weeks

**Part 2 — Document the before/after (30 min)**

```markdown
## Workflow: [Name]

### Current State
Steps:
1.
2.
3.
Time: [estimate]
Pain points:
- Repetitive work:
- Error-prone steps:
- Documentation gap:

### AI-Native Target State
Steps:
1.
2.
3.
Time: [estimate]
What I still own:
-
Quality gate:
- Critical threshold:
- Warning threshold:

### Stack Required
- MCP servers needed:
- Skills to install/create:
- Agent to build (or use from data-engineering/):

### Risk and Mitigations
Risk 1:
Mitigation:
Risk 2:
Mitigation:
```

**Part 3 — The numbers (20 min)**

Estimate:
- Hours saved per week on this workflow
- Hours of setup + learning investment (one-time)
- Break-even point (weeks)

If you can show the ROI calculation, adoption conversations become much easier.

**Part 4 — Write the pitch (30 min)**

Write a 200-word description of this change aimed at your team lead or manager. Structure:
1. The pain we all feel (one sentence)
2. What the new workflow looks like (two sentences)
3. What quality controls are in place (two sentences)
4. The time saving estimate (one sentence)
5. What you'd need to get started (one sentence)

This is the real output of Module 03 — a concrete, defensible proposal for one workflow transformation.
