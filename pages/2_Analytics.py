import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils import get_condition_options

st.set_page_config(page_title="Analytics", page_icon="📊")

def analyze_symptom_patterns(df):
    """Analyze patterns in symptoms data"""
    if df.empty or 'symptoms' not in df.columns:
        return None, None

    # Create a binary matrix of symptoms
    all_symptoms = []
    for symptoms in df['symptoms'].str.split(','):
        if isinstance(symptoms, list):
            all_symptoms.extend([s.strip() for s in symptoms if s.strip()])
    unique_symptoms = sorted(list(set(all_symptoms)))

    symptom_matrix = pd.DataFrame(0, index=range(len(df)), columns=unique_symptoms)
    for i, symptoms in enumerate(df['symptoms'].str.split(',')):
        if isinstance(symptoms, list):
            for symptom in symptoms:
                if symptom.strip() in unique_symptoms:
                    symptom_matrix.iloc[i][symptom.strip()] = 1

    # Calculate correlation matrix
    correlation_matrix = symptom_matrix.corr()
    return correlation_matrix, symptom_matrix

def analytics():
    st.title("Analytics & Insights")

    if st.session_state.data.empty:
        st.info("No data available for analysis. Please add some entries first.")
        return

    # Convert date column to datetime
    df = st.session_state.data.copy()
    df['date'] = pd.to_datetime(df['date'])

    # Condition filter
    selected_condition = st.selectbox(
        "Select Condition to Analyze",
        options=["All Conditions"] + get_condition_options(),
        index=0
    )

    if selected_condition != "All Conditions":
        df = df[df['condition'] == selected_condition]

    if df.empty:
        st.info(f"No data available for {selected_condition}")
        return

    # Time period selector
    time_period = st.selectbox(
        "Select Time Period",
        ["Last Week", "Last Month", "Last 3 Months", "All Time"]
    )

    # Filter data based on time period
    if time_period != "All Time":
        days = {
            "Last Week": 7,
            "Last Month": 30,
            "Last 3 Months": 90
        }
        df = df[df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=days[time_period]))]

    col1, col2 = st.columns(2)

    with col1:
        # Severity over time
        st.subheader("Severity Trend")
        fig_severity = px.line(
            df,
            x='date',
            y='severity',
            color='condition' if selected_condition == "All Conditions" else None,
            title='Severity Trend Over Time'
        )
        st.plotly_chart(fig_severity, use_container_width=True)

        # Common symptoms
        st.subheader("Common Symptoms")
        valid_symptoms = df['symptoms'].dropna().str.split(',').explode()
        if not valid_symptoms.empty:
            symptom_counts = valid_symptoms.value_counts()
            fig_symptoms = px.bar(
                x=symptom_counts.index,
                y=symptom_counts.values,
                title='Symptom Frequency'
            )
            st.plotly_chart(fig_symptoms, use_container_width=True)

    with col2:
        # Common triggers
        st.subheader("Common Triggers")
        valid_triggers = df['triggers'].dropna().str.split(',').explode()
        if not valid_triggers.empty:
            trigger_counts = valid_triggers.value_counts()
            fig_triggers = px.pie(
                values=trigger_counts.values,
                names=trigger_counts.index,
                title='Common Triggers'
            )
            st.plotly_chart(fig_triggers, use_container_width=True)

        # Treatment usage
        st.subheader("Treatment Usage")
        valid_treatments = df['treatment'].dropna().str.split(',').explode()
        if not valid_treatments.empty:
            treatment_counts = valid_treatments.value_counts()
            fig_treatments = px.bar(
                x=treatment_counts.index,
                y=treatment_counts.values,
                title='Treatment Usage'
            )
            st.plotly_chart(fig_treatments, use_container_width=True)

if __name__ == "__main__":
    analytics()