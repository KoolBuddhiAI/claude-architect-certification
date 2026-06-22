# Module 00: Trainer Delivery Guide

## The Trainer's Job in This Module

Your job is NOT to explain AI to data engineers.

Your job is to make them **want** what AI-native workflows give them — before they even know they want it.

The difference: a lecture explains a concept. Good training makes someone feel something first, then gives them the concept to explain what they felt.

**The emotional arc you're building:**
```
Recognition (this is my pain) 
    → Hope (this could be different) 
    → Fear addressed (I won't be replaced) 
    → Pride (my judgment is irreplaceable) 
    → Curiosity (I want to know how)
```

Do not skip steps. Do not rush past the fear. Addressing it directly builds far more trust than glossing over it.

---

## Opening — The Show of Hands (Slides 2–3)

**Do not start with the title slide and your name.** Jump directly to the show of hands.

The questions are designed to create **immediate recognition**:
- "More than five times" — almost everyone raises their hand
- The SQL-during-focus-work question — every data engineer knows this frustration
- The post-production documentation question — they'll groan

When hands go up (and they will), **pause and make eye contact**. Don't rush to slide 3. Let them sit in the recognition for a moment.

Then, quietly: "That's not a skills gap. That's just the job as it exists today."

This is important. You're validating them before you challenge them. They're not doing it wrong. The system is just ready to evolve.

---

## The Story Slide (Slide 4)

This is your most powerful slide. Deliver it as a story, not a bullet point read-out.

**Suggested delivery:**

> "Let me tell you about a data engineer I know. She's been at it for 8 years. She knows her stack cold. Last quarter she got a request at 9am — new Stripe integration, needs to be in the warehouse, reconciled and documented, by end of day. In the past, that was a 6-hour day. She'd be heads-down until 5, stressed, maybe cutting corners on the documentation."
>
> "What happened instead? She spent 30 minutes writing out exactly what the data contract needed to look like — the schema, the quality rules, how to handle nulls, what counted as a duplicate. Then she described it to her agent. The agent built the pipeline. She reviewed the output, caught two edge cases, fixed them, and merged at 11am."
>
> "By 2 o'clock she was working on the architectural decision that had been blocked for two weeks. The one that nobody else on the team could make because it required understanding how three different systems talked to each other."

Pause.

> "That's not a demo. That's a Tuesday."

---

## Handling "But Will AI Take My Job?" (Slides 6–7)

**Do not skip this. Do not be glib about it.**

Some people in the room are quietly scared. They won't say it out loud. Naming it directly — before they do — builds enormous trust.

**Suggested delivery:**

> "I want to take 60 seconds on the thing nobody's said out loud yet, because I know it's in the room."
>
> "Will AI take data engineering jobs?"
>
> "Some. Yes. The ones that are mostly execution — writing the same scripts in different shapes. Those are at risk."
>
> "But here's what's not at risk: the judgment. The person who knows that 'active customer' means completely different things to the Finance team and the Marketing team in your specific company. The person who knows the data source that everyone trusts is actually wrong on Tuesdays because of how the sync runs. The person who says 'we can't ship this yet, the numbers don't look right.'"
>
> "That's not in a model. That's in you. And honestly? Right now it's buried under work that shouldn't require it."

Then move to slide 7. Read it slowly.

---

## The "What's Actually Changing" Slide (Slide 8)

This is the reframe. Don't rush it.

**Key point to land:** The shift is not about you becoming less valuable. It's about where your value gets applied. More of it goes to the decisions. Less of it goes to the execution.

Some trainers find it helpful to draw a quick matrix here:

```
High skill required    │ Currently buried  │ Where you'll live
Low skill required     │ Most of your day  │ Automated away
```

---

## The "This Is Not Vibe Coding" Slide (Slide 9)

This is important for enterprise contexts. There will be skeptics in the room who've seen colleagues generate terrible code and ship it. They need to know you see the distinction.

**Suggested talking point:**

> "I want to be clear about something. What we're building is not 'prompt it and hope it works.' That approach fails in enterprise and we all know why — you can't audit a vibe."
>
> "What we're talking about is structured delegation. You define the standards. You set the quality gates. You review before anything ships. The agent is fast. You are the filter."

---

## Handling Resistance

### "I don't trust AI to write production code"

**Response**: "Good instinct. Neither do I — not without review. In everything we'll cover, agent-generated code goes through a review checklist before it merges. The difference is you're reviewing instead of writing first draft. That's actually faster and often catches more issues."

### "My stack is too specific for any of this to work"

**Response**: "Let's make that concrete in Module 03. Bring the specific workflow you're thinking of and we'll map it. Most resistance to this dissolves when you see the actual tool for your actual stack."

### "This seems like it would take longer to set up than just doing it"

**Response**: "For a one-time script, yes. For anything you do more than twice, no. And the BMAD approach in Module 02 is specifically designed to make the planning phase fast — usually 30–60 minutes before the agent starts executing."

### "What if the agent makes a mistake I don't catch?"

**Response**: "Same question applies to a junior developer. The answer is the same: quality gates, code review, staging environments, rollback plans. We cover all of that in Module 05. The agent doesn't change your quality process — it just changes who writes the first draft."

---

## The 5-Minute Reflection Exercise (Slide 14)

**Do not skip this.** It's not a nice-to-have — it's the bridge to Module 03.

The exercise anchors the abstract ideas to each person's actual job. When they come back to Module 03 with their specific answers, the workflow mapping becomes personal and concrete.

Give them genuinely 5 minutes of silence. Resist the urge to fill the space.

If you're remote: use a shared doc or breakout room.

---

## Timing

Full delivery with discussion: **60–75 minutes**
Without discussion: **40 minutes**

Recommended: run it with discussion. The conversations that happen in the "will AI take my job" section are often the most valuable thing in the room.

---

## Signs This Module Landed

- People are asking specific questions about their own workflows, not abstract AI questions
- The skeptics in the room have moved from "I don't believe this" to "okay, but how does it work with X"
- Someone says "yeah, I've been writing the same pipeline in five different forms for three years"
- People are filling in the reflection exercise with real answers, not generic ones

If you're seeing those signals, proceed. If the room is still skeptical and defensive after the story slide, spend more time on the "fear addressed" and "this is not vibe coding" slides before moving on. Never proceed until the fear is acknowledged and addressed.

---

## Closing

End not with "any questions?" but with:

> "Keep those three answers from the reflection. When we get to Module 03, I'm going to ask you to pull them out. What we do there is take your actual current workflow and map it to what it looks like with the right tools. That's where this stops being abstract."

That creates anticipation for the next module instead of closure on this one.
