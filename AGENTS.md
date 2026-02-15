# Agent Instructions & Skills

## Project Overview
This is a No-Code ML Pipeline Builder with a FastAPI backend and a React (Vite + TypeScript) frontend.

## Tech Stack
- **Backend**: Python 3.10+, FastAPI, Scikit-learn, Pandas.
- **Frontend**: React, TypeScript, Vite, ReactFlow, Zustand.
- **Package Manager**: `pnpm` (Frontend), `pip` (Backend).

## Development Guidelines

### Backend
- **Location**: `backend/`
- **Linting**: Run `flake8 .` to check for style issues.
- **Security**: Run `bandit -r .` to check for security vulnerabilities.
- **Testing**: Run `pytest` to execute the test suite.
- **Dependencies**: Managed in `requirements.txt`.

### Frontend
- **Location**: `frontend/`
- **Setup**: Run `pnpm install`.
- **Linting**: Run `pnpm lint`.
- **Type Checking**: Run `pnpm type-check`.
- **Building**: Run `pnpm build`.
- **Security**: Run `pnpm audit`.

## CI/CD Pipeline
A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every PR and push to main. It checks:
1. **Backend**: Linting (flake8), Security (bandit), Tests (pytest).
2. **Frontend**: Linting (eslint), Type checking (tsc), Security (audit), Build (vite build).

## Agent Skills & Behaviors
- **Security First**: Always check for potential security vulnerabilities (e.g., SQL injection, XSS, insecure dependencies). Use `bandit` and `pnpm audit`.
- **Test-Driven**: verify changes by running existing tests or adding new ones.
- **Code Quality**: Ensure code passes all linting checks.
- **Build Verification**: Verify that the frontend builds successfully before submitting changes affecting the UI.
- **Cloudflare Compatibility**: Ensure the frontend build output is compatible with Cloudflare Pages (output dir: `dist`).

## Aggregated Skills (AGG)
- **Python Expert**: Proficient in FastAPI, Pandas, Scikit-learn.
- **React Expert**: Proficient in React, TypeScript, Vite, Zustand.
- **DevOps Aware**: Understands CI/CD pipelines and deployment targets (Cloudflare Pages).
