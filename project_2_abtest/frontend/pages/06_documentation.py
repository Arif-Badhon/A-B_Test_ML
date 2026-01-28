import streamlit as st

st.set_page_config(page_title="Documentation", page_icon="📚", layout="wide")

st.title("📚 Documentation & Concepts")

with st.expander("🔬 Hypothesis Testing Basics", expanded=True):
    st.markdown("""
    ### What is an A/B Test?
    An A/B test (or randomized controlled trial) is a way to compare two versions of a single variable, typically by testing a subject's response to variant A against variant B, and determining which of the two variants is more effective.
    
    ### Key Terms
    
    *   **Null Hypothesis ($H_0$):** The assumption that there is no change or no difference between the groups.
    *   **Alternative Hypothesis ($H_a$):** The claim that there is a difference or a change.
    *   **P-Value:** The probability of seeing the observed results (or more extreme) if the Null Hypothesis is true. A p-value < 0.05 usually means we 'reject' the null hypothesis.
    *   **Alpha ($\alpha$):** The significance level, usually set at 0.05. It's the risk we are willing to take of a False Positive (Type I Error).
    """)

with st.expander("📏 Effect Size (Cohen's d)"):
    st.markdown("""
    ### Why p-value is not enough?
    A p-value tells you *if* there is a difference, but not *how big* that difference is. With a large enough sample size, even a tiny, meaningless difference can be "statistically significant."
    
    ### Cohen's d
    Cohen's d measures the "practical significance" or the magnitude of the difference. 
    *   **0.2:** Small effect
    *   **0.5:** Medium effect
    *   **0.8:** Large effect
    """)

with st.expander("⚡ Power & Sample Size"):
    st.markdown("""
    ### Statistical Power ($\beta$)
    The probability that the test correctly rejects the null hypothesis when the alternative hypothesis is true. In other words, the ability of the test to detect an effect if it exists. We usually target **80% power**.
    
    ### MDE (Minimum Detectable Effect)
    The smallest effect size that you want to be able to detect with your experiment. Smaller MDEs require much larger sample sizes.
    """)

with st.expander("🛠 Choosing the Right Test"):
    st.markdown("""
    | Metric Type | Data Distribution | Recommended Test |
    | :--- | :--- | :--- |
    | Continuous (e.g. Sales) | Normal | **Welch's T-Test** |
    | Continuous | Non-Normal | **Mann-Whitney U** |
    | Binary (e.g. Conversions) | Bernoulli | **Chi-Square** |
    | Multiple Variations | Any | **ANOVA / Post-hoc** |
    """)

st.info("💡 **Tip**: Always run a power analysis *before* starting your experiment to ensure you have enough data to get meaningful results.")
