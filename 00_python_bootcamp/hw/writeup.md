# HW00 Writeup — Song Analysis

Run `uv run python analysis.py` to generate the results, then answer the five questions
below. Replace each `[your answer here]` with your response.

- Questions 1–3 are factual. One or two sentences is enough.
- Question 4 asks you to reflect on something that surprised you.
- Question 5 asks you to connect what you implemented in Part 1 to the two new tools from Part 2.

---

## Question 1 (2 pts)

**Which genre averaged the most weeks on the Billboard chart, and how many
songs is that average computed from?**

[your answer here]

---

## Question 2 (2 pts)

**Who was the most-streamed artist in the dataset (by total streams across all their songs)?**

[your answer here]

---

## Question 3 (2 pts)

**Which year had the most top-10 hits (songs that peaked at position 10 or better)?**

[your answer here]

---

## Question 4 (4 pts)

**What surprised you about the data?**

Pick one finding from your analysis that was unexpected — something that contradicts what
you assumed going in, or that is more interesting than you expected. Explain:
- What you expected to see, and why.
- What the data actually showed.
- What might explain the difference.

[your answer here]

---

## Question 5 (5 pts)

In Part 1 you implemented `count_occurrences` from scratch using only a plain Python
dict. `collections.Counter`, which you used in Part 2, does the same thing but with
extra conveniences built in.

Answer both parts:

**a)** Walk through, step by step, how you accumulated a running total per genre/artist
in `avg_weeks_by_genre` and `most_streamed_artist`, and how you determined the maximum
in `most_streamed_artist`. Would `collections.Counter` have made any part of this
easier, and if so, which part (drawing on how you'd extend your own `count_occurrences`
to do the same thing)?

**b)** `StreamsRanker` and `LongevityRanker` both subclass `SongRanker` and share its
`rank` method, overriding only `score`. If they did **not** share a common base class —
if you had written two separate, unrelated classes instead — what code would you have
had to duplicate? What does inheritance buy you here?

[your answer here]
