import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from components.api_client import api_client

st.set_page_config(page_title="Run Test", page_icon="🧪", layout="wide")

st.title("🧪 Run A/B Test")

# Experiment Creation
with st.expander("Step 1: Create Experiment", expanded=True):
    name = st.text_input("Experiment Name", value="Marketing Campaign Test")
    col1, col2 = st.columns(2)
    with col1:
        control_name = st.text_input("Control group name", value="Control")
        metric_name = st.text_input("Metric name", value="Conversion Rate")
    with col2:
        treatment_name = st.text_input("Treatment group name", value="Treatment")
        metric_type = st.selectbox("Metric type", ["continuous", "binary", "categorical"])
    
    description = st.text_area("Description")
    
    if st.button("Initialize Experiment"):
        try:
            exp = api_client.create_experiment({
                "name": name,
                "description": description,
                "control_group_name": control_name,
                "treatment_group_name": treatment_name,
                "metric_name": metric_name,
                "metric_type": metric_type
            })
            st.success(f"Experiment '{name}' (ID: {exp['id']}) created!")
            st.session_state['current_exp_id'] = exp['id']
            st.session_state['control_name'] = control_name
            st.session_state['treatment_name'] = treatment_name
        except Exception as e:
            st.error(f"Error initializing experiment: {e}")

# Data Input and Analysis
if 'current_exp_id' in st.session_state:
    st.divider()
    st.subheader(f"Step 2: Input Data for Experiment #{st.session_state['current_exp_id']}")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        st.markdown(f"**{st.session_state.get('control_name', 'Control')} Data**")
        control_data_str = st.text_area("Paste comma-separated values", "10, 12, 11, 13, 10, 12, 11, 13", key="c_data")
    with col_input2:
        st.markdown(f"**{st.session_state.get('treatment_name', 'Treatment')} Data**")
        treatment_data_str = st.text_area("Paste comma-separated values", "15, 17, 16, 18, 15, 17, 16, 18", key="t_data")
        
    if st.button("Run Statistical Analysis", type="primary"):
        with st.spinner("Calculating..."):
            try:
                c_data = [float(x.strip()) for x in control_data_str.split(",") if x.strip()]
                t_data = [float(x.strip()) for x in treatment_data_str.split(",") if x.strip()]
                
                res = api_client.run_experiment(st.session_state['current_exp_id'], c_data, t_data)
                
                st.success(f"Analysis Complete! Conclusion: {res['conclusion']}")
                
                # Display Results
                st.subheader("Results Summary")
                res_col1, res_col2, res_col3, res_col4 = st.columns(4)
                res_col1.metric("P-Value", f"{res['p_value']:.4f}")
                res_col2.metric("Effect Size (Cohen's d)", f"{res['effect_size']:.3f}")
                res_col3.metric("T-Statistic", f"{res['t_statistic']:.3f}")
                res_col4.metric("Status", res['conclusion'])
                
                st.info(f"95% Confidence Interval for difference: **[{res['ci_lower']:.3f}, {res['ci_upper']:.3f}]**")
                
                # Visualizations
                st.divider()
                st.subheader("Visualizations")
                
                df = pd.concat([
                    pd.DataFrame({'Group': st.session_state['control_name'], 'Value': c_data}),
                    pd.DataFrame({'Group': st.session_state['treatment_name'], 'Value': t_data})
                ])
                
                viz_col1, viz_col2 = st.columns(2)
                
                with viz_col1:
                    fig_box = px.box(df, x='Group', y='Value', color='Group', 
                                   title="Distribution Comparison (Box Plot)",
                                   template="plotly_white")
                    st.plotly_chart(fig_box, use_container_width=True)
                
                with viz_col2:
                    fig_hist = px.histogram(df, x='Value', color='Group', barmode='overlay', 
                                          title="Distribution Comparison (Histogram)",
                                          template="plotly_white")
                    st.plotly_chart(fig_hist, use_container_width=True)
                
            except Exception as e:
                st.error(f"Analysis Error: {e}")
else:
    st.info("Please complete Step 1 to start an experiment.")
