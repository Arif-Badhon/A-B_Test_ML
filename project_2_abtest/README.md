# Production-Grade A/B Testing Platform

A complete, full-stack A/B testing platform built with FastAPI, Streamlit, and PostgreSQL.

## 🚀 Quick Start (Docker)

To launch the entire platform:

```bash
cd docker
docker-compose up --build
```

-   **Frontend**: [http://localhost:8501](http://localhost:8501)
-   **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🛠 Tech Stack

-   **Frontend**: Streamlit (Python)
-   **Backend**: FastAPI (Python)
-   **Database**: PostgreSQL
-   **Statistical Analysis**: SciPy, NumPy
-   **Visualization**: Plotly
-   **Deployment**: Docker & Docker Compose
-   **Package Manager**: UV

## 📈 Features

-   **Hypothesis Testing**: Welch's T-Test, Mann-Whitney U, Chi-Square.
-   **Power Analysis**: Sample size, Power, and MDE calculators.
-   **Multiple Testing**: Bonferroni and FDR (Benjamini-Hochberg) corrections.
-   **Experiment Management**: Full CRUD for experiments and result history.
-   **ML Model Comparison**: Statistical comparison of model performance across cross-validation folds.

## 🧪 Testing

To run backend tests locally:

```bash
cd backend
uv pip install -e ".[dev]"
pytest
```

## 📁 Project Structure

-   `backend/`: FastAPI application, statistical services, and database models.
-   `frontend/`: Streamlit UI and multi-page application logic.
-   `docker/`: Dockerfiles and orchestration setup.
