# Ramaz ML Course 2026 — Student Repository

Welcome! This repo holds every assignment for the course. Each module is in its
own folder (`00_python_bootcamp/`, `01_linear_algebra/`, …). Inside each module,
`hw/` is the assignment and (where applicable) `exercises/` is the written
problem set.

You'll work on your **local machine** (recommended) or, if you prefer, in
**GitHub Codespaces** (browser-based VS Code, no local installation needed —
see below), and submit each assignment as a zip uploaded to that assignment's
**Google Drive** folder.

---

## First-time setup

You only do this once, at the start of the year.

### 1. Fork this repo

Click the **Fork** button in the top-right of this repo's GitHub page. This
creates your own copy under your GitHub account. All your work lives on **your
fork** — the upstream repo is read-only to you.

### 2. Clone your fork

```bash
git clone https://github.com/YOUR-USERNAME/ramaz-ml-course-2026-student.git
cd ramaz-ml-course-2026-student
```

### 3. Install Python and `uv`

- **Python 3.11+**, if you don't already have it:
  [python.org/downloads](https://www.python.org/downloads/).
- **`uv`** (the Python package manager the course uses):
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  On Windows, see
  [docs.astral.sh/uv/getting-started/installation](https://docs.astral.sh/uv/getting-started/installation/).

If you get stuck on installation — a PATH issue, a Windows-vs-Mac command
difference, a confusing terminal error — it's completely fine to use an AI
coding assistant (Claude Code, ChatGPT, whatever you have) to help you get
your machine set up. That's just tooling, not the assignment. Once you're
into the actual `hw/` files, stick to what's expected in the writeup.

### 4. Open the folder in your editor

Use VS Code, PyCharm, or whatever you like, and work from its terminal.

### 5. Verify the setup

Navigate into the first assignment folder and run the tests:

```bash
cd 00_python_bootcamp/hw
uv run pytest
```

If you see a list of failing tests (with names like `test_flatten`,
`test_sliding_window`, …), the environment works. Failing tests are expected —
you haven't implemented anything yet.

---

## Alternative: GitHub Codespaces

If you'd rather not install anything locally, you can work entirely in the
browser instead.

1. **Fork** the repo (as in step 1 above).
2. On your fork's page, click the green **`< > Code`** button, switch to the
   **Codespaces** tab, and click **Create codespace on main**.
3. Wait 1–2 minutes for the environment to build. The devcontainer
   automatically installs Python 3.11, `uv`, and all dependencies for every
   released assignment. When it finishes you'll be in a VS Code editor in your
   browser, with a terminal (**View → Terminal**, or `` Ctrl+` `` / `` Cmd+` ``).
4. Verify the setup the same way as above (`cd 00_python_bootcamp/hw && uv run
   pytest`).

Everything else in this README (getting new assignments, submitting, saving
your work) works the same way in Codespaces, with one difference noted below
for saving work, and one for Codespaces' 30-day inactivity limit.

---

## Getting new assignments (during the year)

Two steps:

1. **On GitHub** (in the browser): on your fork's page, click **Sync fork →
   Update branch**. This pulls the teacher's new commits into your fork.
2. **In your terminal** (local or Codespace), run:
   ```bash
   bash setup.sh
   ```
   This pulls the synced changes into your working copy and installs
   dependencies for any new assignment folders.

---

## Submitting

Each assignment submits the same way: build a zip, rename it, and upload it to
that assignment's Drive folder.

From the assignment's `hw/` directory:

```bash
uv run python score.py --zip
```

This creates `hwXX_submission.zip` containing your code and your completed
`writeup.md` — everything needed for grading, in one file. Rename it to
`lastname_firstname_hwXX.zip` and upload it to that assignment's Drive folder,
linked from the assignment's own `hw/README.md`.

You can run `score.py --zip` and re-upload as many times as you like before
the deadline — only your last upload counts. Run `uv run pytest` or `uv run
python score.py` (no `--zip`) anytime to check your progress without
submitting.

---

## Saving your work

Commit and push your work to GitHub regularly — don't wait until you're done
with an assignment.

```bash
git add .
git commit -m "complete part 1"
git push
```

**If you're using Codespaces:** you can do this from the VS Code sidebar
instead of the terminal — click the **Source Control** icon (looks like a
branching tree), stage changes with **+**, write a commit message, then
**Commit** and **Sync Changes**. Also note that your Codespace is deleted
after 30 days of inactivity, so pushing regularly is what actually protects
your work.

---

## Where to start

Open `00_python_bootcamp/hw/README.md`. Each assignment's `README.md` has the
operational details (setup, run, score, submit) and points you at the
assignment content.

---

## Troubleshooting

- **"`uv` is not found"** — close your terminal and open a new one (the
  install added `uv` to your PATH; new terminals pick it up).
- **"Tests can't find a module / `ModuleNotFoundError`"** — run `uv sync` in
  the affected `hw/` folder.
- **"I synced the fork but don't see the new assignment"** — run `bash
  setup.sh` from the repo root.
- **Stuck on a local install issue** — see the note in First-time setup above;
  an AI assistant can help you debug your environment.

**If you're using Codespaces:**
- **"My Codespace won't open / is stuck building"** — wait 2–3 minutes the
  first time. If it still fails, try **Codespaces → Delete** on the broken
  Codespace, then create a new one.

For anything else, ask the teacher in class or via Schoology.
