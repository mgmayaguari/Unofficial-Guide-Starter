from rapidfuzz import fuzz

FUZZY_THRESHOLD = 85  # 0-100. rapidfuzz score below this counts as a miss.

# def judge(question, expects, answer, results) -> bool:
#   """
#   q: 'give', expect: 'give'
#   the expect is in the answer
#   Function to judge whether the answer is correct. The simplest version just checks
#   whether the expected answer is a substring of the actual answer. More sophisticated
#   versions can use fuzzy matching or other techniques to allow for paraphrasing or
#   minor variations in wording.
#   """
#   return expects.lower().strip() in answer.lower()

def judge(question, expects, answer, results) -> bool:
  """
  Same shape as judge() above from lecture, but tolerant of paraphrase: 'expects' doesn't
  have to appear in 'answer' verbatim, just closely enough.

  q: 'give', expect: 'about 120 pages a week', answer: '...roughly 120 pages
  per week...' — a plain substring check misses this, but partial_ratio and
  token_set_ratio both score it high.

  Tried partial_token_set_ratio first and it scored a genuinely wrong answer
  a perfect 100: it reduces both strings to their shared/unique word sets
  before comparing, so a short 'expects' phrase made mostly of common words
  ("the", "is") can look like a full match against an answer that never
  mentions the one word that actually matters ("l-shaped"). Neither
  partial_ratio nor token_set_ratio has that failure on its own, so this
  takes the higher of the two instead — a real paraphrase scores high on at
  least one of them, but stopword overlap alone doesn't fool both.
  """
  expects_clean = expects.lower().strip()
  answer_clean = answer.lower()

  if expects_clean in answer_clean:
    return True

  score = max(
    fuzz.partial_ratio(expects_clean, answer_clean),
    fuzz.token_set_ratio(expects_clean, answer_clean),
  )
  return score >= FUZZY_THRESHOLD

def retrieval_hits(expects, results)-> bool:
  """
  any part my expect in the result
  Returns True if the expected answer is found in the retrieval results.
  The simplest version just checks whether the expected answer is a substring of any of the retrieved chunks.

  More sophisticated versions can use fuzzy matching or other techniques to allow for paraphrasing or minor variations in wording.
  """

  return any(expects.strip().lower() in chunk.lower() for chunk in results)