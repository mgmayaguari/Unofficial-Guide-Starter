# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a question-answering system for `campus_life`, a corpus of short student posts about university life. Ask it something specific - course workloads, dorm noise, laundry room wait times, dining hall rules - and it finds the post that answers it and quotes back from that post, naming the file it came from. Ask it something the corpus doesn't cover, like a general knowledge question, and it says so instead of guessing.

## Chunking Strategy

**Chunk size:** Split by paragraph
**Overlap:** None

I picked `campus_life`, and its documents are short: about 317 characters on
average, one to three paragraphs, and the useful information usually sits in
a single sentence. The starter's fixed 800-character window never even cuts
these documents - running it produces 88 documents and 88 chunks, one whole
document per chunk every time. So the real question wasn't chunk size, it was
whether one post should stay one chunk when it has more than one paragraph in
it.

Splitting on the blank line between paragraphs answered that: it's a boundary
the author already chose, so it never cuts a sentence in half the way a
character count would. I went with no overlap for the same reason overlap
exists in the first place - it exists to hand back a piece of a sentence that
got cut off, and a paragraph break doesn't cut anything off.

I did have to change my first pass. Splitting naively on every paragraph
break turned every document's title line ("The Atrium", "Halden Hall") into
its own chunk, because every one of the 88 documents opens with a short title
line, a blank line, then the real content. That's 88 chunks - about a third
of the total - that were just a few words with nothing to answer from. The
fix was to fold the first paragraph into the second one instead of chunking
it alone, since the title-then-body shape is true of every document in this
corpus, not something a length cutoff needed to guess at. That took the
corpus from 271 chunks down to 183, and the shortest chunk left is a real
sentence ("Expect 4 hours a week outside class.") instead of a bare title.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents
======================================================================
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_340_exams.txt#1` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 2  |  source: course_cs_340_exams.txt#1  |  produced by: chunker.py::split_documents
======================================================================
Start the term project in week three, not week eight; everyone learns this the hard way.
```

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 3  |  source: course_phys_130_workload.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.
```

**Chunk 4** — source: `dining_verrill_street_grill_followup.txt#1` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 4  |  source: dining_verrill_street_grill_followup.txt#1  |  produced by: chunker.py::split_documents
======================================================================
Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.

```

**Chunk 5** — source: `housing_morrow_house.txt#1 ` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 5  |  source: housing_morrow_house.txt#1  |  produced by: chunker.py::split_documents
======================================================================
The good: cheapest housing tier by about $900 a year, and the singles are real singles.
```

## Sample Answer

**Question:** What happens to unused dining dollars at the end of the spring semester?

**Answer:**

```
  (best distance 0.241, cutoff 0.6)

Whatever dining dollars are left in May (at the end of the spring semester) disappear, as they do not roll over to the following autumn (admin_dining_dollars.txt).

Sources retrieved: admin_dining_dollars.txt, admin_meal_plan_changes.txt, dining_halden_hall.txt, dining_north_kitchen.txt, dining_pellew_dining_hall.txt
```

**My relevance cutoff:** 0.6 (the starter default - measured, not moved)

I ran my 5 `QUESTIONS` and the 5 `OUT_OF_SCOPE` questions through `app.py retrieve` and recorded the best distance for each. The two groups came out cleanly separated, with nothing between 0.442 and 0.787:

| Question | In corpus? | Best distance |
|---|---|---|
| Why is the short wing of Innisfree Hall quieter than the rest of the building? | yes | 0.157 |
| What happens to unused dining dollars at the end of the spring semester? | yes | 0.241 |
| How much reading per week should students expect in HIST 118 Modern World History? | yes | 0.273 |
| What's the best time to do laundry in Aldridge Hall to avoid a wait? | yes | 0.278 |
| What do students say is the difference between a work-study job and a non-work-study job? | yes | 0.442 |
| What is the capital of Mongolia? | no | 0.787 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.824 |
| Who won the 1994 World Cup? | no | 0.847 |
| How do I write a for loop in Rust? | no | 0.877 |
| How do I change the oil in a diesel engine? | no | 0.923 |

The starter's default of 0.6 already sits almost in the middle of that gap (0.158 of margin below the lowest in-scope score, 0.187 above the highest out-of-scope one is on the other side of 0.787), so I kept it rather than moving it for no reason. I didn't need the "most corpora land between 0.45 and 0.75" note from `config.py` - my own numbers gave me the gap directly.

## How I Used AI

**1.** Before writing `split_documents`, I asked Claude whether splitting on paragraph breaks with no overlap actually made sense for my corpus, or whether I should add some overlap anyway. It walked through why overlap exists in the first place - to hand back a piece of a sentence that got cut off by a fixed-size window - and pointed out that a paragraph break doesn't cut anything off, so there was nothing for overlap to restore here. Once I agreed with that reasoning, I had it write the paragraph-splitting function. When I ran it, every document's title line ("The Atrium," "Halden Hall") came out as its own useless one-line chunk, which neither of us had caught in the plan - Claude then found that all 88 documents open with that title-then-body shape and fixed the function to fold the title into the first real paragraph instead of chunking it alone.

**2.** For Milestone 4, instead of running `python app.py retrieve "..."` ten times by hand in my terminal, I had Claude run all 5 `QUESTIONS` and all 5 `OUT_OF_SCOPE` questions and report back the best distance for each one. It saved me the manual copy-pasting, but I still read the actual numbers myself and picked the cutoff - Claude just ran the commands and organized the output into the table above.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
