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
Two of my five questions are the ones I'd bet against. My work-study question
depends on a single two-sentence document
(`admin_campus_jobs_and_financial_aid.txt`) that turned out to say the
opposite of what I originally expected — work-study does *not* count against
aid, non-work-study does — so even a perfect retrieval hands the model a
chunk that contradicts my `expects` field. My dining-hall-quality question is
worse: nothing in the corpus discusses food quality at all, only wait times
and hours, so no chunk could ever contain that answer regardless of
retrieval. The other three questions each map to one plain sentence in one
short document (HIST 118's page count, Innisfree's L-shaped wing, Aldridge's
laundry timing), which is exactly the shape `campus_life` documents take —
so I expect those three to be reliable. 4 of 5 is what's left once I assume
one of the two weak questions fails outright. (I'm keeping both weak
questions rather than swapping them for safer ones — a question whose
`expects` field turns out to be wrong, or that has no source at all, is
itself a useful thing to have discovered before I score anything, and it
tells me the fix belongs in `questions.py`, not in retrieval.)

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
I'm holding this to all five, not four, because it isn't really a retrieval
question — it's whether the model follows an instruction it's given every
single time. `generate.py`'s `GROUNDING_INSTRUCTION` unconditionally tells
the model to "name the document your answer came from," and `build_prompt`
labels every retrieved excerpt with `[from <source>]` before it ever reaches
the model. On top of that, the relevance gate in `gate.py` has already
refused anything too thin to answer from, so a question only reaches
`generate()` at all once there's a genuinely relevant, clearly labeled
document in front of it. For this to fail, the model would have to ignore an
explicit, repeated instruction rather than lack the material to follow it —
which is a real risk, but not one I should budget a miss for in advance.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
I haven't run Milestone 4 yet, so I don't have my own measured distances to
point at — this is a prediction, not a report. The five `OUT_OF_SCOPE`
questions (capital of Mongolia, diesel oil changes, a World Cup result,
ibuprofen dosage, a Rust for-loop) share almost no vocabulary with
`campus_life`, which is entirely about one university's dorms, courses, and
dining halls — I'd expect their embeddings to sit far from anything indexed.
`config.py`'s comment on `THRESHOLD` says 0.6 is a starting point and "most
corpora land somewhere between 0.45 and 0.75," so I'm leaving the default in
place for now rather than guessing a tighter number with no data behind it.
4 of 5, not 5 of 5, because one of the out-of-scope questions could plausibly
share incidental vocabulary with a campus document (e.g. a course-related
phrase) and land closer than the rest.

---

## 4. Something about your chunks

At least 4 of 5 sampled chunks are exactly one whole document — no chunk
contains only part of a post, and no chunk silently merges two unrelated
posts into one.

**Why this target:**
`corpora/README.md` says `campus_life` documents average about 317
characters, and `chunker.py`'s own comment on `fallback_split` confirms it:
at the starter's `CHUNK_SIZE = 800` / `CHUNK_OVERLAP = 120`, the corpus comes
out as 88 documents → 88 chunks, because almost nothing reaches 800
characters. So with the current fixed-size strategy, a chunk is already
whichever whole post it came from — the risk isn't mid-sentence truncation,
it's Milestone 3 tempting me to combine short, related posts (like
`dining_pellew_dining_hall.txt` and its `_followup.txt`) to cut down the
chunk count, and stitching two posts together in a way that blurs which
sentence came from which. 4 of 5, not 5 of 5, because a small number of
genuinely-one-topic pairs (like that dining hall post and its follow-up)
combining cleanly would be a reasonable, intentional exception rather than a
defect.



---

## 5. Your choice

For at least 4 of my 5 in-scope questions, the source the system names is not
just present, but actually correct — it's a document that genuinely supports
the answer given, not a plausible-sounding filename pulled from the context
window while the answer itself drifts from what that document says.

**Why this target:**
Criterion 2 only checks that a source gets named; it says nothing about
whether that source is the *right* one. My work-study question is the case
that worries me: `admin_campus_jobs_and_financial_aid.txt` and
`money_jobs.txt` both turn up under a "jobs" search, and the correct document
actually states the reverse of what I first assumed ("count against
financial aid" isn't the direction the source takes). A model that names the
right file but gets the direction backwards, or names the wrong file
entirely because it's topically adjacent, is a more dangerous failure than an
outright refusal — it looks trustworthy and isn't. 4 of 5, not 5 of 5,
because I'm already expecting the work-study and dining-quality questions
from criterion 1 to be the hard cases, and I'd rather set a target I can miss
on a known-weak question than pretend citation accuracy is guaranteed.



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
