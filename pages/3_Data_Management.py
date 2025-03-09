import streamlit as st
import pandas as pd
from data_manager import export_data
from pdf_generator import create_pdf_report
import io

st.set_page_config(page_title="Data Management", page_icon="💾")

def data_management():
    st.title("Data Management")

    # View Data
    st.subheader("View Data")
    if not st.session_state.data.empty:
        st.dataframe(st.session_state.data)
    else:
        st.info("No data available")

    # Export Data
    st.subheader("Export Data")
    if not st.session_state.data.empty:
        export_format = st.radio("Export Format", ["PDF", "CSV", "Excel"])

        # Condition filter for PDF export
        selected_condition = None
        if export_format == "PDF":
            conditions = ["All Conditions"] + list(st.session_state.data['condition'].unique())
            selected_condition = st.selectbox(
                "Select Condition for PDF Report",
                options=conditions,
                index=0
            )

        if st.button("Export Data"):
            if export_format == "PDF":
                # Filter data if a specific condition is selected
                export_data = st.session_state.data.copy()
                if selected_condition != "All Conditions":
                    export_data = export_data[export_data['condition'] == selected_condition]

                pdf_buffer = create_pdf_report(export_data, selected_condition)
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_buffer,
                    file_name="dermatologic_condition_report.pdf",
                    mime="application/pdf"
                )
            elif export_format == "CSV":
                csv = export_data(st.session_state.data, 'csv')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="dermatologic_data.csv",
                    mime="text/csv"
                )
            else:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    st.session_state.data.to_excel(writer, sheet_name='Data', index=False)
                st.download_button(
                    label="Download Excel",
                    data=buffer.getvalue(),
                    file_name="dermatologic_data.xlsx",
                    mime="application/vnd.ms-excel"
                )
    else:
        st.info("No data available to export")

    # Data Cleanup
    st.subheader("Data Cleanup")
    if st.button("Clear All Data", help="Warning: This will delete all recorded data"):
        if st.session_state.data.empty:
            st.warning("No data to clear")
        else:
            st.session_state.data = pd.DataFrame(columns=[
                'date', 'condition', 'severity', 'symptoms', 'triggers',
                'treatment', 'notes'
            ])
            st.success("All data has been cleared")

if __name__ == "__main__":
    data_management()