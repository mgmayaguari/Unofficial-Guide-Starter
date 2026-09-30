# from rapidfuzz import fuzz


def judge(question, expects, answer, results) -> bool:
  """
  q: 'give', expect: 'give'
  the expect is in the answer
  """
  return expects.lower().strip() in answer.lower()


# FUZZY_THRESHOLD = 85  # 0-100. rapidfuzz score below this counts as a miss.


# def fuzzy_judge(question, expects, answer, results) -> bool:
#   """
#   Same shape as judge() above, but tolerant of paraphrase: 'expects' doesn't
#   have to appear in 'answer' verbatim, just closely enough.

#   q: 'give', expect: 'about 120 pages a week', answer: '...roughly 120 pages
#   per week...' — a plain substring check misses this. partial_token_set_ratio
#   treats expects as a bag of words and checks how much of that bag shows up
#   anywhere in answer, so reordering, extra words around it, and small wording
#   changes (about -> roughly) don't cost anything, while an answer missing the
#   actual words in expects still scores low.
#   """
#   expects_clean = expects.lower().strip()
#   answer_clean = answer.lower()

#   return (
#     expects_clean in answer_clean
#     or fuzz.partial_token_set_ratio(expects_clean, answer_clean) >= FUZZY_THRESHOLD
#   )

def retrieval_hits(expects, results)-> bool:
  """
  any part my expect in the result
  Returns True if the expected answer is found in the retrieval results.
  """

  return any(expects.strip().lower() for result in results)