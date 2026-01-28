import streamlit as st
import pandas as pd
from components.api_client import api_client

st.set_page_config(page_title="Results History", page_icon="📜", layout="wide")

st.title("📜 Results History")

try:
    experiments = api_client.get_experiments()
    
    if not experiments:
        st.info("No experiments have been created yet. Go to 'Run Test' to start one!")
    else:
        # Main Table
        df = pd.DataFrame(experiments)
        # Reorder and format columns
        cols = ['id', 'name', 'status', 'metric_name', 'metric_type', 'created_at']
        df_display = df[cols].copy()
        df_display['created_at'] = pd.to_datetime(df_display['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        
        st.subheader("All experiments")
        st.dataframe(df_display, use_container_width=True)
        
        # Detail View
        st.divider()
        st.subheader("Detailed Results")
        
        experiment_options = {f"{e['id']} - {e['name']}": e['id'] for e in experiments}
        selected_label = st.selectbox("Select Experiment to view history", options=list(experiment_options.keys()))
        selected_id = experiment_options[selected_label]
        
        if selected_id:
            results = api_client.get_results(selected_id)
            if results:
                res_df = pd.DataFrame(results)
                res_cols = ['id', 'p_value', 'effect_size', 't_statistic', 'ci_lower', 'ci_upper', 'conclusion', 'computed_at']
                res_display = res_df[res_cols].copy()
                res_display['computed_at'] = pd.to_datetime(res_display['computed_at']).dt.strftime('%Y-%m-%d %H:%M')
                
                st.table(res_display)
                
                # CSV Export
                csv = res_display.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download results as CSV",
                    data=csv,
                    file_name=f"experiment_{selected_id}_results.csv",
                    mime="text/csv",
                )
            else:
                st.warning("This experiment has been initialized but no test has been run yet.")

except Exception as e:
    st.error(f"Could not connect to the API. Is the backend running? ({e})")
