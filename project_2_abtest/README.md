# 📊 Professional A/B Testing Platform & Statistical Inference Lab

This is a production-grade A/B testing framework designed for rigorous statistical analysis of experiments and machine learning models. Built with **FastAPI**, **Streamlit**, and **PostgreSQL**, it provides a complete end-to-end workflow from power analysis to multiple testing correction.

## 🚀 Quick Start (Docker)

To launch the entire platform:

```bash
cd docker
docker-compose up --build
```

-   **Frontend**: [http://localhost:8501](http://localhost:8501)
-   **API Documentation**: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 🎓 Teaching Note: Advanced Statistical Inference for ML Students

This project serves as a practical laboratory for advanced statistical concepts. In the context of Machine Learning, A/B testing is not just about "button colors"—it's the gold standard for model evaluation in production.

### 1. The P-Value Crisis & Effect Size
While p-values are the industry standard, they are often misunderstood. A p-value tells you the probability of seeing your results if there were no difference (Null Hypothesis). However, with enough data, even a microscopic difference becomes "statistically significant."

**Key Lesson:** In this framework, we calculate **Cohen's d**. This measures the *magnitude* of the difference (Practical Significance) rather than just the *existence* of one (Full Service at `backend/services/statistics.py`).

### 2. Welch’s T-Test vs. Student’s T-Test
Most textbooks start with Student’s T-test, which assumes equal variance. In real-world data (conversion rates, latency, etc.), groups rarely have equal variance.

**Key Lesson:** We implement **Welch’s T-Test** as the default. It is more robust and correctly handles unequal variances and unequal sample sizes by adjusting the degrees of freedom via the Welch-Satterthwaite equation.

### 3. Statistical Power & MDE (Minimum Detectable Effect)
Failed experiments are often "Underpowered." If your sample size is too small, you might fail to detect a real improvement (Type II Error).

**Key Lesson:** Use the **Power Analysis Page** to determine your required sample size *before* you start. In ML, this helps you decide if a 1% improvement in accuracy is even detectable given your traffic.

### 4. Multiple Testing Correction (The Look-Elsewhere Effect)
If you test 20 different metrics at a 5% significance level, one of them will likely look "significant" purely by chance (False Discovery).

**Key Lesson:** This platform implements **Bonferroni** and **BH (False Discovery Rate)** corrections. Use these when comparing multiple model variants or multiple KPIs simultaneously.

---

## 🛠 Tech Stack

-   **Frontend**: Streamlit + Plotly (Dynamic visual storytelling)
-   **Backend**: FastAPI (Asynchronous statistical engine)
-   **Database**: PostgreSQL 16 (Relational tracking of results)
-   **Math/Stats**: SciPy & NumPy (Industry-standard computation)
-   **Deployment**: Docker Compose (System reproducibility)

## 📈 Features

-   **Hypothesis Testing**: Welch's T-Test, Mann-Whitney U (non-parametric), Chi-Square (categorical).
-   **Power Analysis**: Sample size, Power, and MDE calculators.
-   **Multiple Testing**: Bonferroni and FDR (Benjamini-Hochberg) corrections.
-   **ML Model Comparison**: Dedicated tool for comparing model performance across cross-validation folds using Paired T-Tests.

## 🧪 Testing

To run the internal verification suite:

```bash
cd backend
uv run --all-extras pytest --cov=services
```

---

## 📁 Project Structure

-   `backend/`: FastAPI application, statistical services, and database models.
-   `frontend/`: Streamlit UI and multi-page application logic.
-   `docker/`: Dockerfiles and orchestration setup.
-   `tests/`: 90%+ coverage unit tests for statistical reliability.
