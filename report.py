from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, tax, regime, old_tax, new_tax, filename="tax_report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("Tax Summary Report (FY 2025-26)", styles["Title"]))
    content.append(Spacer(1, 20))

    # User Data Table
    user_table_data = [
        ["Field", "Value"],
        ["Annual Income", f"₹{data['income']}"],
        ["80C Investment", f"₹{data['80C']}"],
        ["80D Insurance", f"₹{data['80D']}"],
        ["Selected Regime", regime.upper()],
    ]

    table = Table(user_table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black)
    ]))

    content.append(table)
    content.append(Spacer(1, 20))

    # Tax Summary
    content.append(Paragraph("Tax Calculation", styles["Heading2"]))
    content.append(Paragraph(f"Estimated Tax (with cess): ₹{tax}", styles["Normal"]))
    content.append(Spacer(1, 20))

    # Comparison
    content.append(Paragraph("Regime Comparison", styles["Heading2"]))
    content.append(Paragraph(f"Old Regime Tax: ₹{old_tax}", styles["Normal"]))
    content.append(Paragraph(f"New Regime Tax: ₹{new_tax}", styles["Normal"]))

    # Recommendation
    if old_tax < new_tax:
        best = "Old Regime is better"
    elif new_tax < old_tax:
        best = "New Regime is better"
    else:
        best = "Both regimes give same tax"

    content.append(Paragraph(f"Recommendation: {best}", styles["Heading3"]))
    content.append(Spacer(1, 20))

    # Suggestions
    content.append(Paragraph("Tax Saving Suggestions", styles["Heading2"]))
    content.append(Paragraph("• Invest under 80C (₹1.5L limit)", styles["Normal"]))
    content.append(Paragraph("• Take health insurance under 80D", styles["Normal"]))
    content.append(Paragraph("• Use full deduction benefits in old regime", styles["Normal"]))
    content.append(Spacer(1, 20))

    # ITR Steps
    content.append(Paragraph("ITR Filing Steps", styles["Heading2"]))
    content.append(Paragraph("1. Go to Income Tax Portal", styles["Normal"]))
    content.append(Paragraph("2. Login using PAN", styles["Normal"]))
    content.append(Paragraph("3. Select ITR-1", styles["Normal"]))
    content.append(Paragraph("4. Enter income details", styles["Normal"]))
    content.append(Paragraph("5. Add deductions", styles["Normal"]))
    content.append(Paragraph("6. Verify and submit", styles["Normal"]))

    doc.build(content)

    return filename