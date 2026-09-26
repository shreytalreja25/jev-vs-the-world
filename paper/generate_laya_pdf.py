"""
PDF Generation script for compiling the Jev vs. Laya Research Paper
into a formatted PDF document (paper/jev_vs_laya.pdf).
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

from src.config import FIGURES_DIR, PAPER_DIR


class NumberedCanvas(canvas.Canvas):
    """
    Canvas class for dynamically drawing running headers and page footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#444444"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Hosted API vs. Open-Weight Encoder Models: An Empirical Evaluation of Jev and Laya")
            self.setStrokeColor(colors.HexColor("#cccccc"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, footer_text)
        self.drawString(54, 36, "https://github.com/shreytalreja25/jev-vs-the-world.git")
        self.setStrokeColor(colors.HexColor("#cccccc"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * inch - 54, 48)
        
        self.restoreState()


def build_laya_pdf():
    pdf_filename = os.path.join(PAPER_DIR, "jev_vs_laya.pdf")
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Define custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1a202c"),
        alignment=1,
        spaceAfter=10
    )
    
    author_style = ParagraphStyle(
        'DocAuthor',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#2b6cb0"),
        alignment=1,
        spaceAfter=12
    )

    abstract_heading = ParagraphStyle(
        'AbsHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=4
    )

    abstract_text = ParagraphStyle(
        'AbsText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1a365d"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#2b6cb0"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2d3748"),
        leftIndent=12,
        spaceAfter=3
    )

    story = []

    # Title & Authors
    story.append(Paragraph("Hosted API vs. Open-Weight Encoder Models: An Empirical Evaluation of Jev and Laya in Enterprise Decision Architectures", title_style))
    story.append(Paragraph("Shrey Talreja & Antigravity AI<br/><font size=8.5 color='#4a5568'>Ref: Hugging Face Community Guide (September 24, 2026) | Repository: https://github.com/shreytalreja25/jev-vs-the-world.git</font>", author_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e0"), spaceAfter=10))

    # Abstract Box
    abstract_content = [
        [Paragraph("ABSTRACT", abstract_heading)],
        [Paragraph(
            "As machine-native decision layers replace auto-regressive text parsing in enterprise AI workflows, software engineers face a fundamental architectural choice: deploying managed System-One decision APIs such as <b>Jev (TypeSafe AI)</b> or self-hosting open-weight encoder models such as <b>Laya (Apache-2.0)</b>. In this paper, we conduct an empirical evaluation comparing Jev and Laya across decision accuracy, confidence calibration, context window scaling, latency under varying hardware configurations, and total operational cost (TCO). Referencing the JevBench v1.3.0 benchmark dataset (534 decision cases), Jev achieves a composite score of <b>74.4 (#1 ranking)</b> compared to Laya's <b>54.4 (#33 ranking)</b>, with a pronounced gap on complex decision logic (<b>74.1% vs 34.1% hard-case accuracy</b>). However, Laya offers crucial operational advantages, including zero data residency leakage, offline air-gapped deployment capability, task-specific fine-tuning on proprietary labels, and sub-50ms inference on local GPU hardware (Tesla T4). We formalize an Operating Boundary Decision Matrix to guide engineering teams on selecting between hosted APIs and open-weight encoder decision architectures.",
            abstract_text
        )]
    ]
    abs_table = Table(abstract_content, colWidths=[504])
    abs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f7fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(abs_table)
    story.append(Spacer(1, 10))

    # 1. Introduction
    story.append(Paragraph("1. Introduction & Operating Boundaries", h1_style))
    story.append(Paragraph(
        "Modern autonomous software systems rely heavily on typed decision microservices for intent classification, safety guardrail enforcement, dynamic ticket routing, and policy scoring. Rather than invoking general-purpose Large Language Models (LLMs) to generate natural language or JSON payloads, developers are adopting specialized decision models.", body_style
    ))
    story.append(Paragraph(
        "Two primary paradigms have emerged in 2026: (1) <b>Jev (TypeSafe AI)</b>—a managed zero-shot API supporting 64k token contexts and 255 choice options without GPU overhead; and (2) <b>Laya (Apache-2.0)</b>—an open-weight encoder model supporting on-premise execution, task-specific fine-tuning, and strict data residency compliance.", body_style
    ))

    # 2. JevBench v1.3.0 Results Table
    story.append(Paragraph("2. JevBench v1.3.0 Empirical Findings", h1_style))
    table_data = [
        ["Evaluation Metric", "Jev 1.13.0 (Hosted API)", "Laya (Open Weight Encoder)", "Delta"],
        ["Composite Score", "74.4 (#1)", "54.4 (#33)", "+20.0 pts (Jev)"],
        ["Intelligence Score", "85.7", "45.8", "+39.9 pts (Jev)"],
        ["Calibration Score", "82.7", "62.5", "+20.2 pts (Jev)"],
        ["Standard-Case Accuracy (%)", "99.0%", "72.9%", "+26.1% (Jev)"],
        ["Hard-Case Accuracy (%)", "74.1%", "34.1%", "+40.0% (Jev)"],
        ["Context Window Limit", "64,000 tokens", "512 tokens / question", "125x (Jev)"],
        ["Licensing & Hosting", "Managed API", "Open Weights (Apache-2.0)", "Local Control (Laya)"],
    ]

    res_table = Table(table_data, colWidths=[150, 130, 140, 84])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a365d")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(res_table)
    story.append(Spacer(1, 8))

    # Add Figure 4 (JevBench Chart)
    fig4 = os.path.join(FIGURES_DIR, "fig4_jev_vs_laya_scores.png")
    if os.path.exists(fig4):
        story.append(KeepTogether([
            Paragraph("<b>Figure 1: JevBench v1.3.0 Metric Comparisons: Jev vs. Laya</b>", h2_style),
            Image(fig4, width=6.5*inch, height=3.6*inch),
            Spacer(1, 8)
        ]))

    # 3. Decision Boundary Matrix Table
    story.append(Paragraph("3. Operational Decision Matrix", h1_style))
    matrix_data = [
        ["Constraint / Requirement", "Start With", "Architectural Rationale"],
        ["No labeled data or fine-tuning team", "Jev", "Designed for high zero-shot accuracy via managed API."],
        ["Data must stay inside private network", "Laya", "Open weights allow self-hosted, air-gapped deployment."],
        ["Long tickets, documents, or logs", "Jev", "Supports 64k-token request context vs Laya's 512 tokens."],
        ["Multilingual intent routing", "Laya", "Dedicated multilingual checkpoint available for local tuning."],
        ["No GPU operations capacity", "Jev", "No GPU provisioning, checkpoint updates, or serving monitoring."],
    ]

    mat_table = Table(matrix_data, colWidths=[160, 70, 274])
    mat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2b6cb0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(mat_table)
    story.append(Spacer(1, 10))

    # 4. Conclusion
    story.append(Paragraph("4. Conclusion", h1_style))
    story.append(Paragraph(
        "Start with Jev when zero-shot accuracy, 64k context windows, and managed cloud infrastructure are required. Evaluate Laya when open weights, strict on-premise data residency, or proprietary label fine-tuning are central product constraints.", body_style
    ))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated PDF paper at: {pdf_filename}")


if __name__ == "__main__":
    build_laya_pdf()
