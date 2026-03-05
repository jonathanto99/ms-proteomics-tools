# Copilot instructions — MS Protein & Peptide Plotter (MSPP)

Goal: onboard an AI coding agent to be immediately productive in this repository.

1. Big picture
- Backend: Flask app at `programs/mspp_web/backend/app.py` — REST API that ingests DIA‑NN TSVs, uses pandas/numpy and matplotlib (Agg) to return base64 images or binary PNG/ZIP.
- Frontend: React + TypeScript in `programs/mspp_web/frontend/` (Vite). Dev server: :5173; backend: :5000.
- Data flow: frontend uploads TSVs → `POST /api/upload` → backend caches parsed DataFrames → `/api/plot/*` or `/api/export/*` generate figures.

2. Key implementation patterns (inspect these files)
- Data parsing & caching: look in `programs/mspp_web/backend` for DataProcessor — consensus protein logic (require presence in E25 & E100) is central.
- Plot generation: PlotGenerator exposes `_create_*_figure()` helpers and `_fig_to_base64()`; always close figures to avoid memory leaks.
- Organism detection: simple string heuristics (`sp\|` → HeLa, `ECOLI` → E.coli, `YEAST` → Yeast). Update DataProcessor when adding species.

3. Developer workflows
- Backend dev: `cd programs/mspp_web/backend` && `python app.py` (Python 3.14+). Install `requirements.txt`.
- Frontend dev: `cd programs/mspp_web/frontend` && `npm install` && `npm run dev`.
- Production: `cd programs/mspp_web/frontend` && `npm run build` then run backend which serves `frontend/dist`.

4. Conventions & gotchas
- Filename expectations: `report.pg_matrix_E25_*` and `report.pg_matrix_E100_*` (parser tolerant to `E_25`, `E-25`).
- Export settings: PNG exports use dpi=300; reuse `_create_*_figure()` to keep exports consistent.
- Memory: always close figures after conversion (`fig.close()` or `plt.close(fig)`).

5. Extension examples (copy patterns)
- Add export endpoint: follow `/api/export/*` in `app.py` — call `_create_*_figure()` then stream via `io.BytesIO` and `send_file`.
- Add parsing rule: modify organism detection in DataProcessor and add a unit test under `programs/mspp_web/tests/` using sample TSVs.

6. Files to inspect now
- `programs/mspp_web/backend/app.py`
- `programs/mspp_web/backend/*processor*.py` and `*plot*.py` (DataProcessor / PlotGenerator)
- `programs/mspp_web/frontend/src/App.tsx` and `main.tsx`
- `programs/mspp_web/README.md` and `ARCHITECTURE.md` for domain expectations (HeLa ~0, E.coli ~-2, Yeast ~+1)

If you want this file created/updated in the repository, tell me where (repo root or programs/mspp_web/.github) and I will write it. Any section you want expanded before committing?