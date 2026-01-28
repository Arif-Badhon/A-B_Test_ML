import streamlit as st

st.set_page_config(
    page_title="A/B Testing Platform",
    page_icon="📊",
    layout="wide"
)

def main():
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Use the pages below to navigate.")
    
    st.title("📊 A/B Testing Platform")
    
    st.markdown("""
    ## Welcome to the Production-Grade A/B Testing Platform
    
    This platform helps you design, run, and analyze experiments with statistical rigor.
    
    ### 🛠 Features
    
    *   **Statistical Analysis**: Run Welch's t-tests, Mann-Whitney U, and Chi-square tests.
    *   **Power Analysis**: Calculate sample sizes, MDE, and statistical power before you start.
    *   **Result Tracking**: Save and history of all your experiments.
    *   **Visualizations**: Professional-grade charts to communicate results.
    
    ### 🚀 Getting Started
    
    1.  **Calculate Sample Size**: Use the [Power Analysis](Power_Analysis) page to see how many users you need.
    2.  **Run a Test**: Go to [Run Test](Run_Test) to input your data and see results.
    3.  **View History**: Check [Results History](Results_History) to see past experiments.
    """)
    
    st.divider()
    
    st.subheader("Quick Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Confidence Level", "95%")
    with col2:
        st.metric("Target Power", "80%")
    with col3:
        st.metric("Framework", "FastAPI + Streamlit")

if __name__ == "__main__":
    main()
