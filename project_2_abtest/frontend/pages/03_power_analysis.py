import streamlit as st
from components.api_client import api_client

st.set_page_config(page_title="Power Analysis", page_icon="⚡", layout="wide")

st.title("⚡ Power Analysis Calculator")

st.markdown("""
Use these tools to plan your experiment. Calculating the right sample size ensures you have 
enough data to detect meaningful effects without wasting resources.
""")

tab1, tab2, tab3 = st.tabs(["Sample Size Calculator", "Power Calculator", "MDE Calculator"])

with tab1:
    st.header("How many samples do I need?")
    col1, col2 = st.columns(2)
    with col1:
        mde_input = st.number_input("Target Effect Size (Cohen's d)", 
                                   value=0.5, step=0.01, 
                                   help="The smallest effect size you care about detecting.")
        alpha_input = st.slider("Significance Level (Alpha)", 0.01, 0.10, 0.05, 
                               help="Probability of Type I error (False Positive).")
    with col2:
        power_input = st.slider("Target Power", 0.50, 0.99, 0.80, 
                               help="Probability of Type II error (False Negative). Target is usually 0.80.")
    
    if st.button("Calculate Required Sample Size", type="primary"):
        try:
            res = api_client.calculate_sample_size(mde_input, alpha_input, power_input)
            st.success(f"You need **{res['required_sample_size']}** samples per group.")
            st.info(f"Total samples for experiment: {res['required_sample_size'] * 2}")
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.header("What is my current power?")
    col1, col2 = st.columns(2)
    with col1:
        n_input = st.number_input("Current Sample Size (per group)", value=100, step=10)
        mde_p_input = st.number_input("Assumed Effect Size (d)", value=0.5, step=0.01, key="p_mde")
    with col2:
        alpha_p_input = st.slider("Significance Level (Alpha)", 0.01, 0.10, 0.05, key="p_alpha")
    
    if st.button("Calculate Power", type="primary"):
        try:
            res = api_client.calculate_power(n_input, mde_p_input, alpha_p_input)
            power_val = res['power']
            st.metric("Statistical Power", f"{power_val*100:.2f}%")
            if power_val >= 0.8:
                st.success("Power is sufficient (>= 80%)")
            else:
                st.warning("Power is insufficient (< 80%). You may need a larger sample size.")
        except Exception as e:
            st.error(f"Error: {e}")

with tab3:
    st.header("What effect can I detect?")
    col1, col2 = st.columns(2)
    with col1:
        n_mde_input = st.number_input("Sample size (per group)", value=100, step=10, key="mde_n")
        power_mde_input = st.slider("Target Power", 0.50, 0.99, 0.80, key="mde_p")
    with col2:
        alpha_mde_input = st.slider("Significance Level (Alpha)", 0.01, 0.10, 0.05, key="mde_a")
    
    if st.button("Calculate MDE", type="primary"):
        try:
            res = api_client.calculate_mde(n_mde_input, power_mde_input, alpha_mde_input)
            st.metric("Min. Detectable Effect (d)", f"{res['mde']:.3f}")
            st.info("Any effect size smaller than this might go undetected given your sample size.")
        except Exception as e:
            st.error(f"Error: {e}")
