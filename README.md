# No-Code ML Pipeline Builder

Visual, step-based UI to build and run ML workflows without code. Backend uses FastAPI + scikit-learn; frontend uses React (Vite + TypeScript) with Material UI and React Flow.

## Quick start (Windows PowerShell)

### Backend
1. `cd backend`
2. `python -m venv .venv`
3. `.venv\Scripts\Activate.ps1`
4. `pip install -r requirements.txt`
5. `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

### Frontend
1. Open new terminal
2. `cd frontend`
3. `npm install`
4. Create `.env` (optional) with `VITE_API_BASE=http://localhost:8000/api`
5. `npm run dev`

Visit http://localhost:5173 and ensure the backend is running at http://localhost:8000.

### Deploy to GitHub Pages (frontend)
1. Ensure the repo name stays `assignment` or set `VITE_BASE_PATH` accordingly.
2. Push to `main`; GitHub Actions workflow `.github/workflows/deploy-pages.yml` builds `frontend` and publishes to Pages.
3. In repository settings → Pages, select the GitHub Actions source (if not already set).
4. After first deploy, your site will be available at `https://<username>.github.io/assignment/`.
	- Custom domain: add `CNAME` in repo settings; if you add one, also place a `CNAME` file in `frontend/public/` with that domain.
	- SPA fallback: `frontend/public/404.html` redirects to the base path.
	- Robots: `frontend/public/robots.txt` allows all crawlers.

## Features
- Upload CSV/XLSX, preview first 5 rows, view schema
- Select target + optional feature columns
- Add preprocessing steps (StandardScaler / MinMaxScaler) per column or all numeric
- Configure train/test split
- Choose a single model: Logistic Regression or Decision Tree
- Run pipeline; view accuracy, confusion matrix, and feature importance
- React Flow visualization showing Data → Preprocess → Split → Model → Result

## API
- `POST /api/datasets/upload` (multipart file) → dataset metadata + preview
- `POST /api/pipeline/run` with payload `{ dataset_id, target_column, feature_columns?, preprocess[], split{test_size}, model }`

## Notes & Assumptions
- In-memory dataset store (upload again if server restarts)
- Non-numeric targets are label-encoded automatically
- Non-numeric features are one-hot encoded; missing values filled (median/mode)
- Preprocessing applies only to numeric columns; non-numeric selections are skipped with warnings

## Testing tips
- Try the Iris dataset (CSV) to see multi-class confusion matrix
- Adjust split slider and preprocessing to observe metric changes
