import streamlit as st

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


import pandas as pd
from datetime import datetime
from data_manager import load_data, save_data

st.set_page_config(
    page_title="Main",
    page_icon="🔍",
    layout="wide"
)

st.sidebar.markdown("# Main")
st.sidebar.markdown("[Log Entry](1_Log%20Entry)")
st.sidebar.markdown("[Analytics](2_Analytics)")
st.sidebar.markdown("[Data Management](3_Data%20Management)")

def main():
    st.title("Dermatologic Condition Tracker")

    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = load_data()

    # Dashboard layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recent Activity")
        recent_data = st.session_state.data.sort_values('date', ascending=False).head(5)
        if not recent_data.empty:
            for _, row in recent_data.iterrows():
                with st.expander(f"{row['condition']} - {row['date']} - Severity: {row['severity']}"):
                    st.write(f"Symptoms: {row['symptoms']}")
                    st.write(f"Triggers: {row['triggers']}")
                    st.write(f"Treatment: {row['treatment']}")
        else:
            st.info("No entries yet. Start by adding a new log entry!")

    with col2:
        st.subheader("Condition Summary")
        if not st.session_state.data.empty:
            conditions = st.session_state.data['condition'].unique()
            for condition in conditions:
                condition_data = st.session_state.data[st.session_state.data['condition'] == condition]
                with st.expander(f"{condition} Summary"):
                    avg_severity = condition_data['severity'].mean()
                    total_entries = len(condition_data)
                    last_entry = condition_data['date'].max()

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Average Severity", f"{avg_severity:.1f}/10")
                    col2.metric("Total Entries", total_entries)
                    col3.metric("Last Entry", last_entry)
        else:
            st.info("Add entries to see statistics")

if __name__ == "__main__":
    main()
