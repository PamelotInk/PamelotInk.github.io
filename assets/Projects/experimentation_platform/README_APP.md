# Experimentation Platform — Project Overview

This document explains how the app is organized, how it works end-to-end, and how to run and deploy it. It's written for someone new to the project.

---

## 1) Short summary

This repository contains a small experimentation platform: a Streamlit UI (`app.py`) that interacts with a local SQLite database to create experiments, log metrics, and analyze A/B results. The project includes a small `core` package with business logic (`data_manager.py`, `statistical_engine.py`) and database setup scripts in `database/`.

You can run the app locally (Streamlit), view it in your browser at `http://localhost:8501`, and stop it when finished. Helper scripts make start/stop easy; `requirements.txt` contains pinned dependencies for reproducing the environment.

---

## 2) Project structure (what each top-level file/folder is for)

- `app.py` — Streamlit application; UI entrypoint. Uses `core` and `database` code to show experiment creation, logging, and analysis.
- `venv/` — Python virtual environment (do not commit to Git). Activate this before running.
- `core/`
  - `statistical_engine.py` — statistical utilities (mean, A/B calculations, helper analytics).
  - `data_manager.py` — handles DB connections, creating experiments, logging metrics, and queries returning pandas DataFrames.
  - (other helpers can live here)
- `database/`
  - `db_setup.py` — creates the SQLite DB and schema (creates `data/experiments.db`).
- `data/` — contains the local SQLite DB file `experiments.db` (created by the setup script) and any sample datasets.
- `start_streamlit.ps1` / `stop_streamlit.ps1` — helper scripts to start/stop the Streamlit app easily on Windows.
- `requirements.txt` — pinned Python dependencies (created from the venv).
- `README_STREAMLIT.md` — short quick-start for running Streamlit (start/stop, background option).
- `README_APP.md` — this full explanation.

---

## 3) How the pieces work together (data flow)

1. Database setup
   - `database/db_setup.py` creates the SQLite database file and tables: `experiments`, `variants`, `experiment_metrics`.
2. Create experiment (UI or code)
   - The UI (in `app.py`) calls `ExperimentDataManager.create_experiment(...)` to insert rows into `experiments` and `variants`.
   - Dates are stored as ISO-formatted text (safe across Python versions).
3. Log metrics
   - `ExperimentDataManager.log_metrics(...)` stores daily metrics (impressions, conversions, revenue) in `experiment_metrics` for a variant.
4. Analysis
   - `core/statistical_engine.py` provides statistical helpers. The Streamlit UI calls these with aggregated metrics from `get_experiment_results()`.
   - Example analytics: conversion rates, lift, p-value, required sample size, etc.
5. UI
   - `app.py` presents forms to create experiments and log metrics, and shows A/B results and charts using Plotly.

---

## 4) Running the app locally (step-by-step)

1) Open PowerShell in the project root (where `app.py` is located).
2) Activate the environment:

```powershell
. .\venv\Scripts\Activate.ps1
```

3) If you haven't created the DB yet, run:

```powershell
.\venv\Scripts\python.exe database\db_setup.py
```

4a) Development (visible logs):

```powershell
.\venv\Scripts\streamlit.exe run app.py --server.headless true
```

Leave that terminal open to see logs; stop with Ctrl+C.

4b) Quick background start (recommended for occasional use):

```powershell
.\start_streamlit.ps1
# then open http://localhost:8501
# when finished
.\stop_streamlit.ps1
```

Notes:
- If you see a ``streamlit.pid`` file, the stop helper will use it to stop the app.
- If you started Streamlit manually in a terminal, stop it in that terminal (Ctrl+C).

---

## 5) Deploying / Sharing the app (interview friendly options)

- Streamlit Cloud (recommended for interviews)
  - Push your repo to GitHub (public or private with Streamlit Cloud plan), then deploy at https://share.streamlit.io.
  - Streamlit Cloud will install from `requirements.txt` and give you a public URL — easiest and cleanest for interviews.

- Temporary public URL (ngrok)
  - Run app locally and in another terminal run `ngrok http 8501` to get a public URL to share for a short time.
  - Stop ngrok after the interview.

- Local-only (screen-share)
  - For privacy or local-only demos, just open http://localhost:8501 and share your screen in Zoom/Teams.

---

## 6) Running on login / reminders (optional)

- You can create a Scheduled Task in Windows to run `start_streamlit.ps1` at logon or at a specific daily time. That starts the background process automatically.
- I provide the start/stop scripts so you can keep full manual control — recommended for occasional use.

---

## 7) Developer notes & suggestions

- Tests: add unit tests for `core/statistical_engine.py` (mean, p-value calculations) and database integration tests for `data_manager`.
- Packaging: add a small `app_config` or `.env` if you later add secrets or external DBs.
- Logs: if you need logs from the background run, modify `start_streamlit.ps1` to redirect stdout/stderr to files; I can add that (or I already created a variant if you want it).

---

## 8) Quick troubleshooting

- If `http://localhost:8501` shows nothing, check:
  - Is the app running? `Get-Process -Name streamlit` or check `streamlit.pid`.
  - Are you running the correct venv? Activate before starting.
  - Is another app using port 8501? Try `--server.port 8502`.

- If you see Python date deprecation warnings, the code stores ISO-formatted strings now and pandas reads them with `parse_dates`, so it should be OK.

---

## 9) Interview checklist (two options)

A) Public (easy)
- Push to GitHub, create `requirements.txt` (already created), deploy to Streamlit Cloud. Share the URL on your resume or during the interview.

B) Local + share
- Start with `start_streamlit.ps1`, run `ngrok http 8501` to create a temporary public URL, share it during the interview, then stop both after.

---

If you want, I can now:
- Add logs to `start_streamlit.ps1` (stdout/err files).
- Create a Scheduled Task for daily reminder or autostart at logon.
- Prepare a minimal GitHub README and guide to deploy to Streamlit Cloud.

Tell me which of those you want next and I'll implement it.
