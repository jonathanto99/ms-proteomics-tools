# Agentic AI instructions — MS Protein & Peptide Plotter (MSPP)

Goal: Onboard AI coding agents to be immediately productive in this repository.

## 1. Big picture
- **Backend:** Flask app at `programs/mspp_web/backend/app.py` — REST API that ingests DIA‑NN TSVs, uses pandas/numpy and matplotlib (Agg) to return base64 images or binary PNG/ZIP.
- **Frontend:** React + TypeScript in `programs/mspp_web/frontend/` (Vite). Dev server: :5173; backend: :5000.
- **Data flow:** frontend uploads TSVs -> `POST /api/upload` -> backend caches parsed DataFrames -> `/api/plot/*` or `/api/export/*` generate figures.
- **Other Tools:** Standalone GUI tools and notebooks live in `programs/python/`.

## 2. Agent Behavior & Rules of Engagement
- **Plan First:** For complex tasks, propose a concise strategy before modifying files.
- **Search First:** Do not guess paths or imports. Search the workspace to verify existing patterns.
- **Validate Autonomously:** Never assume a change works. Always run `pytest tests/` or frontend linting before concluding your turn.
- **Dependencies:** Do not add new `npm` or `pip` packages without explicit user permission.
- **Security:** Never hardcode secrets or absolute paths. Use environment variables.
- **Communication:** Be extremely concise. Avoid conversational filler. Output the minimal amount of text needed to explain your action. 

## 3. Key implementation patterns (inspect these files)
- **Data parsing & caching:** look in `programs/mspp_web/backend` for DataProcessor — consensus protein logic (require presence in E25 & E100) is central.
- **Plot generation:** PlotGenerator exposes `_create_*_figure()` helpers and `_fig_to_base64()`; always close figures to avoid memory leaks.
- **Organism detection:** simple string heuristics (`sp\|` -> HeLa, `ECOLI` -> E.coli, `YEAST` -> Yeast). Update DataProcessor when adding species.

## 4. Developer workflows & Scripts
- **Setup:** Prefer using `python scripts/setup/setup_dev.py` or platform-specific `.sh`/`.ps1` scripts to instantiate the environment. `pixi` is also supported (`pixi run start`).
- **Backend dev:** `cd programs/mspp_web/backend` && `python app.py` (Python 3.14+). Or use `python scripts/launch/launcher.py`.
- **Frontend dev:** `cd programs/mspp_web/frontend` && `npm install` && `npm run dev`.
- **Production:** `cd programs/mspp_web/frontend` && `npm run build` then run backend which serves `frontend/dist`.

## 5. Code Quality & Tooling (Strict Requirements)
- **Python Formatting & Linting:** Use `ruff` (`ruff format .` and `ruff check --fix .`). Line length is 100 characters. `mypy` is used for type checking.
- **Python Docstrings:** All new functions and classes must include clear docstrings.
- **Frontend Linting:** Use `npm run lint` (ESLint) and `npm run type-check` (tsc) in the `frontend` directory.
- **Testing:** Backend tests are in `tests/`. Always run `pytest tests/` after modifications. Ensure you add tests for new features (`pytest-cov` is active).
- **Commits:** Follow conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).

## 6. Conventions & gotchas
- **Filename expectations:** `report.pg_matrix_E25_*` and `report.pg_matrix_E100_*` (parser tolerant to `E_25`, `E-25`).
- **Export settings:** PNG exports use dpi=300; reuse `_create_*_figure()` to keep exports consistent.
- **Memory:** always close figures after conversion (`fig.close()` or `plt.close(fig)`).

## 7. Extension examples (copy patterns)
- **Add export endpoint:** follow `/api/export/*` in `app.py` — call `_create_*_figure()` then stream via `io.BytesIO` and `send_file`.
- **Add parsing rule:** modify organism detection in DataProcessor and add a unit test under `tests/` using sample TSVs.

## 8. Files to inspect now
- `programs/mspp_web/backend/app.py`
- `programs/mspp_web/backend/*processor*.py` and `*plot*.py` (DataProcessor / PlotGenerator)
- `programs/mspp_web/frontend/src/App.tsx` and `main.tsx`
- `pyproject.toml` (for tooling configurations)
- `programs/mspp_web/README.md` for domain expectations (HeLa ~0, E.coli ~-2, Yeast ~+1)
