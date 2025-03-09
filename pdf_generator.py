from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
from datetime import datetime

def create_pdf_report(df, selected_condition=None):
    """Generate a PDF report from the tracking data"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    title = "Dermatologic Condition Report"
    if selected_condition:
        title += f" - {selected_condition}"
    elements.append(Paragraph(title, title_style))

    # Report date
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20
    )
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", date_style))

    # Summary statistics
    if not df.empty:
        summary_style = ParagraphStyle(
            'Summary',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        
        elements.append(Paragraph("Summary Statistics:", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        avg_severity = df['severity'].mean()
        total_entries = len(df)
        date_range = f"{df['date'].min()} to {df['date'].max()}"
        
        elements.append(Paragraph(f"Average Severity: {avg_severity:.1f}/10", summary_style))
        elements.append(Paragraph(f"Total Entries: {total_entries}", summary_style))
        elements.append(Paragraph(f"Date Range: {date_range}", summary_style))
        elements.append(Spacer(1, 20))

        # Data table
        elements.append(Paragraph("Detailed Entries:", styles['Heading2']))
        elements.append(Spacer(1, 12))

        # Prepare table data
        table_data = [['Date', 'Condition', 'Severity', 'Symptoms', 'Triggers', 'Treatment']]
        for _, row in df.iterrows():
            table_data.append([
                row['date'],
                row['condition'],
                str(row['severity']),
                row['symptoms'],
                row['triggers'],
                row['treatment']
            ])

        # Create and style table
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        elements.append(table)

    else:
        elements.append(Paragraph("No data available for the report.", styles['Normal']))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
