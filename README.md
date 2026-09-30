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
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks stay one document | 4 of 5 | 1 of 5 | 1 of 5 | 1 of 5 | MISS |
| 5. Every answer names the correct source | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | MET |

Criteria 1, 3, and 4 don't change between runs — retrieval and chunking are
deterministic, so one measurement is the whole measurement for those, the
same way the out-of-scope gate results don't vary. Only criteria 2 and 5
depend on what the model actually wrote, and those held steady across all
three runs anyway (source: `results/run_2026-09-29_2131.md`, scored with the
original strict `scorer.judge`).

### Criterion 1 — Retrieved chunk contains the answer

Produced by `store.py::search`, question from `questions.py::QUESTIONS`. The top result is the chunk that answers the question:

```
Question: Why is the short wing of Innisfree Hall quieter than the rest of the building?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.1573     housing_innisfree_hall_noise.txt Noise levels in Innisfree Hall  Asked about this a l...
2   0.4440     housing_old_brewhouse_noise.txt  Noise levels in Old Brewhouse  Asked about this a lo...
3   0.4597     housing_fenwick_court_noise.txt  Noise levels in Fenwick Court  Asked about this a lo...
4   0.4688     housing_innisfree_hall.txt       Innisfree Hall — what it's actually like  Transferre...
5   0.5293     housing_morrow_house_noise.txt   Noise levels in Morrow House  Asked about this a lot...

Gate: best distance 0.157 is under the 0.6 cutoff
```

The full text of that top chunk (`housing_innisfree_hall_noise.txt#0`) is "Noise levels in Innisfree Hall — Asked about this a lot so writing it down. Moderate; the building is l-shaped and the short wing is much quieter." — the answer is right there.

### Criterion 2 — Every answer names a source

Produced by `generate.py::answer_from_chunks`, from `results/run_2026-09-29_2131.md`:

```
Whatever is left in May disappears (it does not roll over from the spring to the following autumn).

Source: admin_dining_dollars.txt
```

### Criterion 3 — Gate stops out-of-corpus questions

Produced by `run_eval.py::check_out_of_scope`, from `results/run_2026-09-29_2131.md`:

```
| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.787 | refused |
| How do I change the oil in a diesel engine? | 0.923 | refused |
| Who won the 1994 World Cup? | 0.847 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.824 | refused |
| How do I write a for loop in Rust? | 0.877 | refused |
```

### Criterion 4 — Chunks stay one document

Produced by `chunker.py::split_documents`, a random sample of 5 chunks (seed 42):

```
housing_tamsin_court_laundry.txt#0  whole document? False  (191 of 286 chars)
'Laundry in Tamsin Court\n\nMachines take in-unit washer-dryer. There are eight washers and six dryers for the building, which is the wrong ratio and means the dryers back up on Sunday evenings.'

course_cs_210_exams.txt#0  whole document? False  (159 of 237 chars)
'CS 210 Data Structures — assessment\n\nTwo midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.'

admin_housing_lottery.txt#0  whole document? True  (397 of 397 chars)
"On the housing lottery\n\nThe housing lottery is not random in the way most people assume. Rising sophomores get a number drawn at random, but juniors and seniors are ordered by accumulated credit hours first, and only tie-break randomly. That means a senior who took summer courses reliably beats a senior who didn't. Numbers come out the second week of March and selection runs over four evenings."

course_phys_130_exams.txt#0  whole document? False  (127 of 194 chars)
'PHYS 130 Mechanics — assessment\n\nThree midterms, no final, plus a lab practical. Not curved, but the lowest midterm is dropped.'

course_math_220.txt#2  whole document? False  (112 of 383 chars)
'The one piece of advice: the problem sets are the course; the lectures make sense afterwards rather than during.'
```

Only 1 of 5 is the whole document — the other 4 are single paragraphs of a longer document, which is what `split_documents` is supposed to do for multi-paragraph posts. The criterion's wording (written before Milestone 3 existed) doesn't match that on purpose; see Diagnoses below.

### Criterion 5 — Every answer names the correct source

Produced by `generate.py::answer_from_chunks`, from `results/run_2026-09-29_2131.md` — this is the one that fails it:

```
Based on the provided documents, there is no mention of *why* the short wing is quieter, only that it is. (Source: housing_innisfree_hall_noise.txt)
```

The named source is real and it's the right file, but the claim in the answer is false — that same document's text (see Criterion 1 above) says plainly "the building is l-shaped and the short wing is much quieter." The citation points at the right place; the model just didn't use what was in it.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | Target was 4 of 5. All 5 questions had the answer in their top retrieved chunk, and retrieval doesn't change between runs, so 5 of 5 held all three times, not just once. |
| 2 | Every answer names a source | MET | Target was 5 of 5. Every answer in all three runs named a source file, so it held all three times, not just on average. |
| 3 | Gate stops out-of-corpus questions | MET | Target was 4 of 5. All 5 `OUT_OF_SCOPE` questions got refused, and the gate is a fixed comparison against a distance that doesn't change between runs, so this is one measurement, not three lucky ones. |
| 4 | Chunks stay one document | MISS | Target was 4 of 5. Only 1 of 5 sampled chunks was a whole document - the other 4 are single paragraphs of longer posts, which is what the paragraph-splitting chunker does on purpose. The criterion's wording assumed the pre-Milestone-3 fallback chunker, where a chunk and a document were the same thing; once I actually split by paragraph, that stopped being true for any document with more than one paragraph. This is a MISS against what I wrote, not a sign the chunker is broken. |
| 5 | Every answer names the correct source | MET | Target was 4 of 5, and it landed at exactly 4 of 5 in all three runs - not 4, 3, 4. The one failure is the same question every time (Innisfree Hall noise): the model cites the right file but the answer's own claim ("there is no mention of why") is false, which I'm counting as a wrong citation because the source doesn't actually support the answer given. Because the same question fails the same way every run, this is a real, repeatable defect, not run-to-run noise - worth a Diagnoses entry even though the target technically held. |

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

**Criterion 4 miss — chunking stage, but not a chunking bug.**

The miss traces to chunking, but the mechanism isn't a defect in `split_documents` - it's that the target sentence describes a chunker I no longer have. I wrote "chunks are exactly one whole document" back when the starter's fixed 800-character window was still running, and on `campus_life` that window never fires: 88 documents in, 88 chunks out, one per document, every time. Once I replaced it with paragraph splitting in Milestone 3, that stopped being true on purpose - a 3-paragraph post now produces 3 chunks, none of which is the whole document. Of the 88 documents in this corpus, most have more than one paragraph, so a random sample of chunks is mostly going to land on "part of a post," not "the whole post." That's exactly what the 1-of-5 sample showed: the one hit (`admin_housing_lottery.txt#0`) is whole only because that document happens to be a single paragraph. I'm not treating this as something to fix in `chunker.py` — the paragraph splitting is doing what I want (see Chunking Strategy above). It's the criterion that's stale, not the code.

**Criterion 5's one failure — generation stage, and it's real.**

Every run, the Innisfree Hall noise question gets the exact right chunk: `housing_innisfree_hall_noise.txt#0` retrieves at distance 0.157, and its full text is "Moderate; the building is l-shaped and the short wing is much quieter." That's the answer, sitting in the prompt, labeled with its source, every single time. And every single time, across all 3 runs, the model answers that the documents don't explain *why* the short wing is quieter - flatly wrong, and wrong the same way each time, which rules out a one-off hiccup. The failure is entirely in generation, not retrieval or chunking: the model has the causal clause ("l-shaped... short wing is much quieter") right in front of it and doesn't connect it to a "why" question, maybe because the sentence states the fact rather than spelling out "because it's l-shaped, the short wing is quieter." It's a pattern worth watching for on other causal ("why") questions, not just this one, since none of my other four questions ask "why" - I only have one data point, but it's a clean one.

I didn't miss anything else, and none of my other targets look set low in hindsight. Criterion 5's 4-of-5 target is the one I'd tighten if I had more than 5 test questions - 4 of 5 is generous enough that one reproducible generation bug still counts as a MET, and this run log is proof that "held the target" and "no real bugs" aren't the same thing.

## The Improvement

**What I changed:** Tightened `generate.py`'s `GROUNDING_INSTRUCTION` with one new rule, aimed squarely at the Innisfree bug: *"A 'why' question is answered whenever the documents state a plausible cause in the same breath as the effect, no matter the punctuation joining them - a period, a semicolon, or 'and' all count equally, and the word 'because' doesn't need to appear at all... Treat two facts stated side by side as cause and effect if that's the only relationship that makes sense, and state the connection yourself."* The example I used in the instruction is a made-up one ("the road is icy; traffic is moving slowly") rather than the actual Innisfree sentence, on purpose - putting the real answer in the prompt would make the test question pass by feeding it the answer, not by fixing the underlying behavior.

**Why I picked it:** This is the fix my own diagnosis named directly: the model was handed the exact chunk containing "the building is l-shaped and the short wing is much quieter" and still said no explanation was given, every single time, across all 3 runs of the original diagnosis. That's a generation-stage problem - retrieval and chunking were never at fault - so the fix belongs in the prompt that tells the model how to read what it's given, not in retrieval or chunking.

### Run Log — After

`python run_eval.py --label after`, same fixed scorer, same semantic-only retrieval - full transcript in `results/run_2026-09-29_2334_after.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks stay one document | 4 of 5 | 1 of 5 | 1 of 5 | 1 of 5 | MISS |
| 5. Every answer names the correct source | 4 of 5 | 5 of 5 | 4 of 5 | 5 of 5 | MET |

Real output - the Innisfree question, all 3 runs, next to the same question from the pre-fix baseline:

```
Before (results/run_2026-09-29_2317_before.md) — all 3 runs identical:
Based on the provided documents, there is no explanation given for why the
short wing of Innisfree Hall is quieter; it only states that it is quieter
(housing_innisfree_hall_noise.txt).

After (results/run_2026-09-29_2334_after.md):
— run 1: The documents do not provide a reason for why the short wing of
  Innisfree Hall is quieter than the rest of the building; they only state
  that the building is l-shaped and the short wing is much quieter
  (housing_innisfree_hall_noise.txt).
— run 2: The documents do not contain information explaining why the short
  wing of Innisfree Hall is quieter than the rest of the building
  (housing_innisfree_hall_noise.txt).
— run 3: The documents do not provide a reason for why the short wing of
  Innisfree Hall is quieter; they only state that the building is l-shaped
  and the short wing is much quieter (housing_innisfree_hall_noise.txt).
```

**Did it help?**

Partially, and I want to be precise about what actually changed rather than round it up to a clean win. Before the fix, this question failed identically in all 3 runs - the model never once mentioned the l-shape. After the fix, it mentions the l-shape in 2 of 3 runs (run 1 and run 3), and criterion 5's per-run score moved from a flat 4-of-5 every time to 5, 4, 5 - real, measurable improvement in how often the fact makes it into the answer.

But it's not a clean fix, and I'm not calling it one. Look closely at runs 1 and 3: the model states the l-shape fact, but wraps it in a sentence that simultaneously *denies* giving a reason - "The documents do not provide a reason... they only state that the building is l-shaped and the short wing is much quieter." That's self-contradictory: it names the reason in the same breath as claiming there isn't one. It passes the scorer, because the expected phrase is there as a substring, but a person reading that sentence would still come away confused about whether the system thinks it answered the question. And run 2 shows the original failure mode didn't go away, it just got less frequent — the instruction is a nudge the model sometimes follows, not a guarantee.

So: measurably better, still not reliable, and the specific failure mode it partially fixed came back in an odd half-fixed shape (right fact, wrong framing) that a stricter scorer than mine would probably still catch. If I kept iterating, the next step wouldn't be a bigger prompt change — it'd be figuring out why the model hedges even when it has the right fact in hand, which might be more about `MODEL` (`gemini-3.5-flash-lite`) than about the prompt.

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
