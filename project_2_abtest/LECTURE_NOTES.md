# 🎓 Lecture Notes: Statistical Inference in Machine Learning Production

## 1. Introduction: Why A/B Testing for ML?
In Machine Learning, we often rely on offline metrics (Accuracy, F1, RMSE). However, **offline success ≠ online success**. A model with higher precision might fail in production due to user behavior shifts, latency, or feedback loops. 

A/B testing is the standard for **Online Evaluation**. This project provides the statistical infrastructure to ensure that any observed improvement is not just due to random noise.

---

## 2. The Statistical Engine: What's Happening Under the Hood?

### A. Welch's T-Test (The Workhorse)
Located in `backend/services/statistics.py`, we use the Welch's T-test instead of the standard Student's T-test.
- **Why?** In practice, the variance of your "Control" model (running for months) and your "Treatment" model (new, perhaps less stable) is rarely the same. 
- **The Magic:** It adjusts the degrees of freedom using the **Welch-Satterthwaite equation**, making it much more reliable for unequal sample sizes and variances.

### B. Cohen's d (Effect Size)
A p-value tells you *if* a difference exists. Cohen's d tells you *how much* it matters.
- For ML engineers, this helps answer: "Is this model 0.1% more accurate (statistically significant but practically tiny) or 5% better (a massive win)?"

### C. Paired T-Tests for Cross-Validation
In the `Model Comparison` page, we use a **Paired T-test**.
- **The Concept:** When you run K-fold cross-validation, Model A and Model B are tested on the *exact same data folds*. This reduces variance and allows us to use a paired test, which is much more powerful for detecting small differences between two algorithms on a fixed dataset.

---

## 3. The Power Analysis Protocol
Before deploying a new model, you MUST ask: "How many users do I need to see if this model is better?"

### The Triangle of Power:
1. **Alpha ($\alpha$):** Confidence (usually 0.05).
2. **Power ($1-\beta$):** Probability of detecting an effect (usually 0.80).
3. **MDE (Minimum Detectable Effect):** The smallest lift in performance that justifies a deployment.

**The ML Intuition:** If your "Target MDE" is a 0.5% lift in conversion, and the calculator says you need 1 million users, but your app only has 10,000—you know ahead of time that you won't be able to prove the model is better within a reasonable timeframe.

---

## 4. Practical Application: Evaluating Your Custom Models

### Scenario 1: Offline Selection (Before Production)
You have built a new XGBoost model and want to compare it against a Random Forest baseline.
1. Run a 10-fold Cross-Validation for both models on the same data.
2. Store the accuracy/F1 score for each fold in two lists.
3. Use the **Model Comparison Tool** in this platform. 
4. **Conclusion:** If the p-value is < 0.05, the winning model is statistically superior across your validation sets.

### Scenario 2: Online A/B Test (The "Grand Finale")
You want to see if your recommendation engine actually increases revenue.
1. Deploy the "Treatment" model to 50% of users.
2. Use the **Backend API** (`POST /api/experiments/{id}/run`) to log the performance data (e.g., daily revenue per user) from both groups.
3. The platform will automatically calculate the lift, confidence intervals, and significance.

---

## 5. Integrating with Your ML Pipeline
You can integrate this platform into your CI/CD or MLOps pipeline:

```python
import requests

# After running your automated pipeline...
results = {
    "control_data": [0.82, 0.81, 0.83], # Baseline model scores
    "treatment_data": [0.85, 0.86, 0.84] # New model scores
}

# Call the statistical engine via API
response = requests.post("http://localhost:8001/api/experiments/1/run", json=results)
print(response.json()["conclusion"]) # "Significant" or "Not Significant"
```

## 6. Summary for Students
*   **Don't p-hack:** Use Multiple Testing Correction if you are comparing 10 models at once.
*   **Look at CI:** If the Confidence Interval is huge, your result is unstable even if it's "significant."
*   **Power first:** Always calculate sample size requirements *before* you run an online experiment.
