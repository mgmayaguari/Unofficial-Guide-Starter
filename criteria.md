# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Each of my five questions now maps to one plain sentence in one short
document - HIST 118's page count, Innisfree's L-shaped wing, Aldridge's
laundry timing, the work-study/financial-aid rule, and the dining dollars
rollover. That's exactly the shape `campus_life` documents take, so in
principle retrieval should find all five. I'm still not asking for 5 of 5,
because two pairs of documents share a lot of vocabulary - the two dining
posts, and `admin_campus_jobs_and_financial_aid.txt` next to `money_jobs.txt` - and with 88 short, similar-sounding posts in this corpus, a close neighbor
grabbing the top spot instead of the exact right document is a realistic way
for one question to miss even when the corpus itself isn't the problem.
(Earlier drafts of the work-study and dining questions had a wrong `expects`
value and no supporting document at all - both are now fixed in
`questions.py`, so this criterion no longer has to plan around them failing
outright.)

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
This isn't a retrieval problem, it's whether the model follows one simple,
repeated instruction. `generate.py` labels every excerpt it hands the model
with `[from <source>]` and tells it flat out to "name the document your
answer came from." The gate has already blocked any question too thin to
answer, so by the time a question reaches the model, a clearly labeled,
relevant document is already sitting in the prompt. Naming it is just
following an instruction, not finding something hard - so I expect all five,
not four.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" -
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
I haven't run Milestone 4 yet, so this is a guess, not a measurement. My five
`OUT_OF_SCOPE` questions (capital of Mongolia, diesel oil changes, a World
Cup result, ibuprofen dosage, a Rust for-loop) are generic world facts with
almost no words in common with `campus_life`, which is entirely about one
university's dorms, courses, and dining halls - I expect them to sit far away
from anything in the index. `config.py` already suggests `THRESHOLD = 0.6` as
a reasonable starting point for most corpora, so I'm leaving it there instead
of inventing a tighter number with no data behind it yet. 4 of 5, not 5 of 5,
because one out-of-scope question could still get lucky and share a
coincidental word with a campus document (say, "course" or "week") and land
closer than the rest.

---

## 4. Chunks stay one document

At least 4 of 5 sampled chunks are exactly one whole document - no chunk
contains only part of a post, and no chunk silently merges two unrelated
posts into one.

**Why this target:**
`campus_life` documents average about 317 characters, well under the
starter's 800-character chunk size - so today, every chunk is already a
whole post; nothing gets cut mid-sentence. The real risk shows up in
Milestone 3, if I start merging short, related posts (like
`dining_pellew_dining_hall.txt` and its `_followup.txt`) to cut down the
chunk count - that's where sentences from two different posts could end up
blurred together in one chunk. 4 of 5, not 5 of 5, because merging a
genuinely-one-topic pair like that dining hall post and its follow-up is a
reasonable choice, not a defect, so I don't want a perfect score to force me
into treating every merge as a failure.

> **Revised in unit 2:** At least 4 of 5 sampled chunks are cut on a
> paragraph boundary, not mid-sentence, and no chunk contains text from two
> different documents.
>
> **Why revised:** I wrote the original assuming the starter's fallback
> chunker — where a chunk and a document were the same size on this corpus,
> so "whole document" was a real, measurable thing. Milestone 3 replaced
> that with paragraph splitting on purpose: a 3-paragraph post is *supposed*
> to become 3 chunks now, so "exactly one whole document" stopped being
> something a working chunker could satisfy for any document with more than
> one paragraph. Sampling 5 chunks against the literal original wording got
> 1 of 5 (`results/run_2026-09-29_2131.md`), not because anything is cut
> wrong, but because the target described a chunker I no longer have. The
> revised wording tests the thing I actually care about — no sentence cut in
> half, no two posts blurred into one chunk — which the same sample passes
> 5 of 5.

---

## 5. Every answer names the correct source

For at least 4 of my 5 in-scope questions, the source the system names is not
just present, but actually correct - it's a document that genuinely supports
the answer given, not a plausible-sounding filename pulled from the context
window while the answer itself drifts from what that document says.

**Why this target:**
Criterion 2 only checks that *a* source gets named - not that it's the right
one. My work-study question is the case that worries me most:
`admin_campus_jobs_and_financial_aid.txt` and `money_jobs.txt` both come up
under a "jobs" search, and it would be easy for a model to cite the wrong one
of the two, or cite the right one while getting the direction backwards. A
confident answer with the wrong citation is worse than a refusal, because it
looks trustworthy and isn't. 4 of 5, not 5 of 5, because with two
similar-sounding "jobs" documents in the corpus, I'd rather leave room for
that one mix-up than pretend citation accuracy is guaranteed.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
