# HW00 — Python Bootcamp

**Prerequisites:** Basic Python familiarity (variables, loops, conditionals, functions)

This assignment reviews the Python patterns we'll rely on throughout the course — lists,
dicts, sets, higher-order functions, and classes — and gives you a first taste of data
analysis with plain Python: reading a CSV, tallying with `Counter`, and ranking with a
small class hierarchy.

---

## Submission

Run this from the `hw/` directory:

```bash
uv run python score.py --zip
```

It creates `hw00_submission.zip` with exactly the right files inside.
Rename it to `lastname_firstname_hw00.zip` and upload it to the
[HW00 submission folder](https://drive.google.com/drive/folders/1Euh19DolU-VHmpdUcvLbnmiAA1a2pqVA).

---

## Setup

Open this folder in your editor.

**One-time setup for the whole course.** You need `uv`, which manages both Python and every
package this course uses. Install it once:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen your terminal, then check it worked:

```bash
uv --version
```

You do **not** need to install Python yourself. The repo pins the version in `.python-version`,
and `uv sync` below downloads it for you the first time. Every module in the course uses the same
three commands as this one.

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the tests to see where you stand:**
   ```bash
   uv run pytest
   ```

3. **Check your score:**
   ```bash
   uv run python score.py
   ```

4. **Score a specific part only:**
   ```bash
   uv run python score.py lists      # Part 1
   uv run python score.py dicts      # Part 2
   uv run python score.py sets       # Part 3
   uv run python score.py hof        # Part 4
   uv run python score.py classes    # Part 5
   uv run python score.py songs      # Part 6
   ```

---

## Parts

### Part 1: Python Basics (`python_basics.py`) — 56 pts

Implement 18 functions and 2 classes across five sections:

| Section | Topic | Points |
|---------|-------|--------|
| 1.1 | Lists | 17 |
| 1.2 | Dicts | 13 |
| 1.3 | Sets | 5 |
| 1.4 | Higher-order functions | 11 |
| 1.5 | Classes | 10 |

Read each function's docstring — it tells you exactly what to implement and shows
examples. The examples in the docstring match some of the test cases.

### Part 2: Song Analysis (`analysis.py` + `writeup.md`) — 17 pts (code) + 15 pts (writeup)

Implement `load_songs`, the `SongRanker` class hierarchy, and three `Counter`-based
aggregation functions in `analysis.py`. The dataset columns (the schema) are documented
at the top of `analysis.py`, and you can open `data/songs.csv` to see the raw data. Then
run the analysis script to print results:

```bash
uv run python analysis.py
```

Use the printed output to answer the five questions in `writeup.md`.

---

## Files

| File | What to do |
|------|------------|
| `python_basics.py` | Implement all functions (look for `raise NotImplementedError` — replace with your code) |
| `analysis.py` | Implement `load_songs`, `SongRanker`/`StreamsRanker`/`LongevityRanker`, and the three `Counter`-based functions |
| `writeup.md` | Answer the five analysis questions in full sentences |

**Do not modify:** `test_python_basics.py`, `test_analysis.py`, `conftest.py`, `pyproject.toml`

---

## Tips

- Work through the sections in order — later problems sometimes build on earlier ones.
- **Test one function at a time** — don't wait until everything is done:
  ```bash
  uv run pytest -k TestFlatten          # just the flatten tests
  uv run pytest -k TestSlidingWindow    # just the sliding_window tests
  ```
- The test failure messages are designed to tell you exactly what went wrong — read them.
- If you're stuck on `analysis.py`, look at how the `csv` module can hand you each row
  already split into named fields, rather than a flat list of strings — and how
  `collections` offers a dict-like way to tally things.

---

## Saving your work

Your files are saved on your own machine as you edit. **Commit and push your work to GitHub so
it is backed up and you can pick it up on another machine.**

You can do this entirely from the VS Code sidebar — no terminal needed:

1. Click the **Source Control** icon in the left sidebar (it looks like a branching tree)
2. Click **+** next to each changed file to stage it
3. Type a short commit message (e.g. `"complete part 1"`)
4. Click **Commit**, then **Sync Changes**

Your work is now saved to your GitHub fork. Get into the habit of doing this whenever
you finish a work session.

