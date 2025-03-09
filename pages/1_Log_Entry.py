import streamlit as st
from datetime import datetime
import pandas as pd
from utils import (
    get_symptom_options, get_trigger_options,
    get_treatment_options, get_condition_options
)
from data_manager import save_data

st.set_page_config(page_title="Log Entry", page_icon="📝")

def log_entry():
    st.title("Log New Entry")

    with st.form("log_entry_form"):
        # Condition selection
        condition = st.selectbox(
            "Condition Type",
            options=get_condition_options(),
            help="Select the type of condition you're tracking"
        )

        # Date selection
        date = st.date_input(
            "Date of occurrence",
            value=datetime.now(),
            max_value=datetime.now()
        )

        # Severity slider
        severity = st.slider(
            "Severity Level",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Mild, 10 = Severe"
        )

        # Symptoms multiselect
        symptoms = st.multiselect(
            "Symptoms",
            options=get_symptom_options(),
            default=None
        )

        # Triggers multiselect
        triggers = st.multiselect(
            "Triggers",
            options=get_trigger_options(),
            default=None
        )

        # Treatment multiselect
        treatment = st.multiselect(
            "Treatment Used",
            options=get_treatment_options(),
            default=None
        )

        # Notes text area
        notes = st.text_area(
            "Additional Notes",
            placeholder="Enter any additional observations or notes..."
        )

        submitted = st.form_submit_button("Save Entry")

        if submitted:
            new_entry = pd.DataFrame([{
                'date': date.strftime('%Y-%m-%d'),
                'condition': condition,
                'severity': severity,
                'symptoms': ', '.join(symptoms) if symptoms else '',
                'triggers': ', '.join(triggers) if triggers else '',
                'treatment': ', '.join(treatment) if treatment else '',
                'notes': notes
            }])

            st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
            save_data(st.session_state.data)
            st.success("Entry saved successfully!")

if __name__ == "__main__":
    log_entry()