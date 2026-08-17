# HW00 Writeup — Song Analysis

Run `uv run python analysis.py` to generate the results, then answer the five questions
below. Replace each `[your answer here]` with your response.

- Questions 1–3 are factual. One or two sentences is enough.
- Question 4 asks you to reflect on something that surprised you.
- Question 5 asks you to connect what you implemented in Part 1 to what pandas is doing.

---

## Question 1 (2 pts)

**Which genre averaged the most weeks on the Billboard chart?**

Afrobeats was the genre that averages the most weeks on the Billboard chart

---

## Question 2 (2 pts)

**Who was the most-streamed artist in the dataset (by total streams across all their songs)?**

Taylor swift was the most streamed artist in the dataset with 6.56 billion streams.

---

## Question 3 (2 pts)

**Which year had the most top-10 hits (songs that peaked at position 10 or better)?**

2026 was the year that had the most top 10 hits with 26.

---

## Question 4 (4 pts)

**What surprised you about the data?**

Pick one finding from your analysis that was unexpected — something that contradicts what
you assumed going in, or that is more interesting than you expected. Explain:
- What you expected to see, and why.
- What the data actually showed.
- What might explain the difference.

I expected to see a genre such as rock, country, or pop, to have the most average weeks on chart by genre, because those are typically cosindered the most "popular" genres, at least in my mind. They did have quite high amounts of weeks, but afrobeats having 30 was a shocker to me. From what I can tell, fans of genres such as pop basically have no attention span so a new song replaces a previous one pretty quickly, while Afrobeats is much more internationally popular, as well as being extremely popular in the United States (some songs I did not know were considered afrobeats before this)

---

## Question 5 (5 pts)

In Part 1 you implemented `group_by` from scratch using only Python dicts and lists.
Pandas' `groupby()` does something conceptually similar, but at a much larger scale.

Answer both parts:

**a)** What data structure do you think `groupby` uses internally to organize the rows?
Walk through how you think it works step by step, drawing on your own `group_by`
implementation.

**b)** When you call `df.groupby("genre")["weeks_on_chart"].mean()`, what is pandas
doing? Describe each step — how the data gets grouped, and how the mean is computed —
in your own words.

a) I personally don't know what this groupby would use, but the first data structure that comes to mind for me would be a weird kind of heap, where the groups are parents and the children are the values (perhaps heaps of heaps). The idea is that the root is either representative of the dataframe as a whole or the specific group (such as genre), and then the children are the individual genres, and their children are the different rows that have that genre.

b) I kind of cheated by learning this when I was looking up how groupby works, it's something like "split apply combine". Pandas splits up the rows by their genre into mini-dataframes of each genre, applies the mean calculation to the weeks_on_chart values, and then recombines all the mini-dataframes back into one big series with the genres as indices and the values as the values.