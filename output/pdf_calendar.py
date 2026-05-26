from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from langsmith import traceable
from io import BytesIO
from graph.state import DayEntry
from datetime import datetime


@traceable(name="generate_calendar_pdf")
def generate_calendar_pdf(calendar: list[DayEntry], month: str) -> bytes:
    """Generate a PDF calendar and return as bytes."""

    # Create PDF in memory
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=20,
        alignment=1
    )

    # Title
    title = Paragraph(f"📅 Content Calendar - {month}", title_style)

    # Create table data
    headers = ["Day", "Date", "Platform", "Content Type", "Topic", "Notes"]
    data = [headers]

    for day_entry in calendar:
        row = [
            str(day_entry["day"]),
            day_entry["date"],
            day_entry["platform"],
            day_entry["content_type"],
            day_entry["topic"],
            day_entry["notes"],
        ]
        data.append(row)

    # Create table with adjusted column widths for full text
    table = Table(data, colWidths=[0.5*inch, 0.8*inch, 0.9*inch, 1*inch, 3.5*inch, 1.3*inch])

    # Style table
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),

        # Data rows
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    # Footer
    footer_text = Paragraph(
        f"<i>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Content Strategy Agent</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
    )

    # Build PDF
    elements = [title, Spacer(1, 0.3*inch), table, Spacer(1, 0.2*inch), footer_text]
    doc.build(elements)

    # Get PDF bytes
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
