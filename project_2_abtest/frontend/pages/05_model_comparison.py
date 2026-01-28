import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
import plotly.graph_objects as go

st.set_page_config(page_title="Model Comparison", page_icon="🤖", layout="wide")

st.title("🤖 Model Comparison Tool")

st.markdown("""
Compare two trained models using cross-validation results. We use a **Paired T-Test** 
to determine if one model is significantly better than the other across the same data folds.
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Model A")
    model_a_name = st.text_input("Model A Name", "Random Forest")
    model_a_data_str = st.text_area("Accuracies per fold (comma-separated)", "0.82, 0.84, 0.81, 0.83, 0.82")
with col2:
    st.subheader("Model B")
    model_b_name = st.text_input("Model B Name", "XGBoost")
    model_b_data_str = st.text_area("Accuracies per fold (comma-separated)", "0.85, 0.87, 0.84, 0.86, 0.85")

if st.button("Run Comparison", type="primary"):
    try:
        a = [float(x.strip()) for x in model_a_data_str.split(",") if x.strip()]
        b = [float(x.strip()) for x in model_b_data_str.split(",") if x.strip()]
        
        if len(a) != len(b):
            st.error("Error: The number of folds must be the same for both models to perform a paired t-test.")
        elif len(a) < 2:
            st.error("Error: Need at least 2 folds for comparison.")
        else:
            t_stat, p_val = stats.ttest_rel(a, b)
            mean_a = np.mean(a)
            mean_b = np.mean(b)
            diff = mean_b - mean_a
            
            st.divider()
            st.subheader("Analysis Results")
            
            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric(f"Mean {model_a_name}", f"{mean_a:.4f}")
            res_col2.metric(f"Mean {model_b_name}", f"{mean_b:.4f}")
            res_col3.metric("Difference", f"{diff:.4f}", delta=f"{diff:.4f}")
            
            st.write(f"**P-Value**: `{p_val:.5f}`")
            
            if p_val < 0.05:
                winner = model_b_name if diff > 0 else model_a_name
                st.success(f"✅ **Significant Difference Found!** {winner} is performing significantly better (alpha=0.05).")
                st.info(f"**Action Recommendation**: Deploy **{winner}** to production.")
            else:
                st.warning("⚠️ **No Significant Difference Found.** The observed difference might be due to random noise.")
                st.info("**Action Recommendation**: Either model is acceptable. Consider other factors like latency or interpretability.")
            
            # Box plot comparison
            fig = go.Figure()
            fig.add_trace(go.Box(y=a, name=model_a_name, boxpoints='all', jitter=0.3))
            fig.add_trace(go.Box(y=b, name=model_b_name, boxpoints='all', jitter=0.3))
            fig.update_layout(title="Model Accuracy Distribution Across Folds", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Calculation Error: {e}")
