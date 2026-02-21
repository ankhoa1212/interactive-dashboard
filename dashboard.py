import streamlit as st
import pandas as pd
import os

from load_data import DB_FILE, main as load_data_main
from initial_analysis import get_cell_frequency_data
from statistical_analysis import statistical_analysis
from data_subset_analysis import data_subset_analysis

st.set_page_config(page_title="Immune Cell Analysis Dashboard", layout="wide")

def get_cell_frequency_df():
    """Get cell frequency data as a DataFrame for display in the dashboard."""
    data = get_cell_frequency_data(DB_FILE)
    return pd.DataFrame(data)

def main():
    """Main function to run the Streamlit dashboard."""
    st.sidebar.header("Data Management")  # sidebar button for reloading data if needed
    if st.sidebar.button("Load Data from CSV"):
        import subprocess
        with st.sidebar.status("Loading data from cell-count.csv..."):

            if result.returncode == 0:
                st.sidebar.success("Data loaded successfully.")
            else:
                st.sidebar.error("Failed to load data")
                st.sidebar.write(result.stderr)

    st.sidebar.header("Statistical Test")  # sidebar option for changing statistical test if needed
    test_type = st.sidebar.radio("Select Test Type", ["Mann-Whitney U", "t-test"], index=0)
    test_type_key = 'u' if test_type == "Mann-Whitney U" else 't'

    st.title("Immune Cell Analysis Dashboard")
    st.markdown("Analysis of immune cell frequencies in patients treated with different therapies.")

    st.divider()
    st.header("Cell Population Relative Frequency Summary")
    df = get_cell_frequency_df()
    summary_cols = ['sample', 'total_count', 'population', 'count', 'percentage', 'sample_type', 'condition', 'treatment', 'response']
    st.dataframe(df[summary_cols], use_container_width=True)

    st.divider()
    st.header("Statistical Analysis")
    stats_df = statistical_analysis(return_df=True, test_type=test_type_key)
    if stats_df is not None and not stats_df.empty:
        st.dataframe(
            stats_df[['population', 'responder_mean', 'non_responder_mean', 'p_value', 'significant']],
            use_container_width=True
        )
        # Show boxplot
        if os.path.exists('response_comparison.png'):
            st.image('response_comparison.png', caption='Cell Population Relative Frequencies: Responders vs Non-Responders', width=900)
        else:
            st.warning('Boxplot image not found.')
    else:
        st.info("No statistical analysis data available.")

    st.divider()
    st.header("Data Subset Analysis")
    subset_data = data_subset_analysis(return_dict=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### By Response")
        st.dataframe(subset_data['response_counts'], use_container_width=True)
    with col2:
        st.markdown("#### By Project")
        st.dataframe(subset_data['project_counts'], use_container_width=True)
    with col3:
        st.markdown("#### By Sex")
        st.dataframe(subset_data['sex_counts'], use_container_width=True)
    st.divider()
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("Total Subjects", subset_data['unique_subjects'])
    m_col2.metric("Total Samples", subset_data['unique_samples'])


if __name__ == "__main__":
    load_data_main()  # Load data from CSV into the database
    statistical_analysis()  # Run statistical analysis to generate the boxplot image
    main()
