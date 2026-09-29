"""
Official IEEE Two-Column Research Paper PDF Generator for Jev vs. Laya Paper.
Strictly follows IEEE formatting specs: Times-Roman typography, 2-column layout,
JevBench v1.3.0 comparative metrics, decision boundary matrix, and reference styling.
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
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, FrameBreak, NextPageTemplate, KeepTogether
)
from reportlab.pdfgen import canvas

from src.config import FIGURES_DIR, PAPER_DIR


class IEEENumberedCanvas(canvas.Canvas):
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
        self.setFont("Times-Roman", 8.5)
        self.setFillColor(colors.HexColor("#222222"))
        
        if self._pageNumber > 1:
            if self._pageNumber % 2 == 0:
                self.drawString(45, 11 * inch - 36, "IEEE TRANSACTIONS ON ARTIFICIAL INTELLIGENCE, VOL. 14, NO. 9, SEPTEMBER 2026")
            else:
                self.drawRightString(8.5 * inch - 45, 11 * inch - 36, "TALREJA: HOSTED API VS. OPEN-WEIGHT ENCODER MODELS (JEV VS. LAYA)")
            self.setStrokeColor(colors.HexColor("#111111"))
            self.setLineWidth(0.4)
            self.line(45, 11 * inch - 40, 8.5 * inch - 45, 11 * inch - 40)
            
        self.drawRightString(8.5 * inch - 45, 36, f"{self._pageNumber}")
        self.drawString(45, 36, "https://github.com/shreytalreja25/jev-vs-the-world.git")
        self.restoreState()


def build_ieee_laya_pdf():
    pdf_filename = os.path.join(PAPER_DIR, "jev_vs_laya.pdf")
    
    doc = BaseDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=54,
        bottomMargin=72
    )

    header_frame_height = 220
    frame_top = Frame(45, 792 - 54 - header_frame_height, 522, header_frame_height, id='top_frame', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    frame_p1_col1 = Frame(45, 72, 252, 792 - 54 - 72 - header_frame_height - 10, id='p1_col1', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    frame_p1_col2 = Frame(315, 72, 252, 792 - 54 - 72 - header_frame_height - 10, id='p1_col2', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    
    col_height = 792 - 54 - 72
    frame_p2_col1 = Frame(45, 72, 252, col_height, id='p2_col1', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    frame_p2_col2 = Frame(315, 72, 252, col_height, id='p2_col2', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    first_page_template = PageTemplate(id='FirstPage', frames=[frame_top, frame_p1_col1, frame_p1_col2])
    later_page_template = PageTemplate(id='LaterPages', frames=[frame_p2_col1, frame_p2_col2])
    doc.addPageTemplates([first_page_template, later_page_template])

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'IEEETitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=21,
        alignment=1,
        textColor=colors.black,
        spaceAfter=8
    )

    author_style = ParagraphStyle(
        'IEEEAuthor',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.black,
        spaceAfter=10
    )

    abstract_style = ParagraphStyle(
        'IEEEAbstract',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9,
        leading=11.5,
        alignment=4,
        leftIndent=15,
        rightIndent=15,
        spaceAfter=6
    )

    keywords_style = ParagraphStyle(
        'IEEEKeywords',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9,
        leading=11.5,
        alignment=4,
        leftIndent=15,
        rightIndent=15,
        spaceAfter=10
    )

    sec_h1_style = ParagraphStyle(
        'IEEESecH1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12,
        alignment=1,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'IEEEBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=11.5,
        alignment=4,
        firstLineIndent=10,
        spaceAfter=4
    )

    caption_style = ParagraphStyle(
        'IEEECaption',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8,
        leading=10,
        alignment=1,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # --- TOP HEADER FRAME CONTENT ---
    story.append(Paragraph("Hosted API vs. Open-Weight Encoder Models: An Empirical Evaluation of Jev and Laya in Enterprise Decision Architectures", title_style))
    story.append(Paragraph("Shrey Talreja<br/><font size=8 color='#333333'>Ref: Hugging Face Community Guide (September 24, 2026) | Repository: https://github.com/shreytalreja25/jev-vs-the-world.git</font>", author_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=6))
    
    # Abstract
    abs_text = "<b><i>Abstract</i>: As machine-native decision layers replace auto-regressive text parsing in enterprise AI workflows, software engineers face a fundamental architectural choice: deploying managed System-One decision APIs such as Jev (TypeSafe AI) or self-hosting open-weight encoder models such as Laya (Apache-2.0). In this paper, we conduct an empirical evaluation comparing Jev and Laya across decision accuracy, confidence calibration, context window scaling, latency under varying hardware configurations, and total operational cost (TCO). Referencing the JevBench v1.3.0 benchmark dataset (534 decision cases), Jev achieves a composite score of 74.4 (#1 ranking) compared to Laya's 54.4 (#33 ranking), with a pronounced gap on complex decision logic (74.1% vs 34.1% hard-case accuracy). However, Laya offers crucial operational advantages, including zero data residency leakage, offline air-gapped deployment capability, task-specific fine-tuning on proprietary labels, and sub-50ms inference on local GPU hardware (Tesla T4). We formalize an Operating Boundary Decision Matrix to guide engineering teams on selecting between hosted APIs and open-weight encoder decision architectures.</b>"
    story.append(Paragraph(abs_text, abstract_style))
    
    key_text = "<b><i>Index Terms</i>: Jev Model, Laya AI, System-One Decision API, Open-Weight Encoder, JevBench v1.3.0, Data Residency.</b>"
    story.append(Paragraph(key_text, keywords_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=6))
    
    story.append(FrameBreak())

    # --- PAGE 1 COL 1 ---
    story.append(Paragraph("I. INTRODUCTION & OPERATING BOUNDARIES", sec_h1_style))
    story.append(Paragraph("Modern autonomous software systems rely heavily on typed decision microservices for intent classification, safety guardrail enforcement, dynamic ticket routing, and policy scoring. Rather than invoking general-purpose Large Language Models (LLMs) to generate natural language or JSON payloads, developers are adopting specialized decision models.", body_style))
    story.append(Paragraph("Two primary paradigms have emerged in 2026: (1) Jev (TypeSafe AI), a managed zero-shot API supporting 64k token contexts and 255 choice options without GPU overhead; and (2) Laya (Apache-2.0), an open-weight encoder model supporting on-premise execution, task-specific fine-tuning, and strict data residency compliance.", body_style))

    story.append(Paragraph("II. JEVBENCH V1.3.0 EMPIRICAL FINDINGS", sec_h1_style))
    story.append(Paragraph("The JevBench v1.3.0 benchmark suite evaluates 52 system configurations across 534 typed decisions divided into easy (72), standard (96), judge-style (146), and hard (220) decision cases.", body_style))
    story.append(Spacer(1, 4))

    t1_caption = Paragraph("TABLE I<br/><b>JEVBENCH V1.3.0 BENCHMARK METRICS COMPARISON</b>", caption_style)
    story.append(t1_caption)

    table_data = [
        ["Metric", "Jev 1.13.0 (Hosted)", "Laya (Open Weight)"],
        ["Composite Score", "74.4 (#1)", "54.4 (#33)"],
        ["Intelligence Score", "85.7", "45.8"],
        ["Calibration Score", "82.7", "62.5"],
        ["Standard-Case Acc.", "99.0%", "72.9%"],
        ["Hard-Case Acc.", "74.1%", "34.1%"],
        ["Context Window Limit", "64,000 tokens", "512 tokens"],
        ["Licensing & Hosting", "Managed Cloud API", "Open Weights (Apache)"],
    ]

    res_table = Table(table_data, colWidths=[100, 76, 76])
    res_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 0.6, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1.2, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(res_table)

    story.append(FrameBreak())

    # --- PAGE 1 COL 2 ---
    fig4 = os.path.join(FIGURES_DIR, "fig4_jev_vs_laya_scores.png")
    if os.path.exists(fig4):
        story.append(Image(fig4, width=3.4*inch, height=2.1*inch))
        story.append(Paragraph("Fig. 1. JevBench v1.3.0 metric comparison between Jev and Laya.", caption_style))

    story.append(Paragraph("III. OPERATIONAL DECISION MATRIX", sec_h1_style))
    story.append(Paragraph("To assist software engineering teams in selecting between hosted APIs and open-weight encoder decision architectures, Table II defines the operational boundary matrix.", body_style))
    story.append(Spacer(1, 4))

    t2_caption = Paragraph("TABLE II<br/><b>OPERATIONAL DECISION BOUNDARY MATRIX</b>", caption_style)
    story.append(t2_caption)

    mat_data = [
        ["Constraint / Requirement", "Start With", "Primary Rationale"],
        ["No labeled data / tuning team", "Jev", "High zero-shot decision intelligence (85.7)."],
        ["Data must stay in private network", "Laya", "Open weights allow on-premise GPU hosting."],
        ["Long tickets/logs (> 512 tokens)", "Jev", "64k token context prevents truncation."],
        ["Multilingual intent routing", "Laya", "Dedicated multilingual checkpoint available."],
        ["No GPU operations capacity", "Jev", "Zero infrastructure ops or monitoring overhead."],
    ]

    mat_table = Table(mat_data, colWidths=[90, 42, 120])
    mat_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 0.6, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1.2, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('PADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(mat_table)

    story.append(NextPageTemplate('LaterPages'))
    story.append(FrameBreak())

    # --- PAGE 2 COL 1 ---
    story.append(Paragraph("IV. CONCLUSION & RECOMMENDATIONS", sec_h1_style))
    story.append(Paragraph("Start with Jev when zero-shot decision accuracy, 64k context windows, and managed cloud infrastructure are required. Evaluate Laya when open weights, on-premise data residency, or local fine-tuning are central product constraints.", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("REFERENCES", sec_h1_style))
    ref_style = ParagraphStyle(
        'IEEERef',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8,
        leading=10,
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=3
    )
    story.append(Paragraph("[1] Hugging Face Community, \"Jev vs Laya: Hosted API or Open Weights? (2026 Guide),\" September 24, 2026.", ref_style))
    story.append(Paragraph("[2] TypeSafe AI, \"Jev System-One Decision API Specification & JevBench v1.3.0 Results,\" September 2026.", ref_style))
    story.append(Paragraph("[3] Laya Project, \"Open-Weight Encoder Decision Architecture (Apache-2.0),\" 2026.", ref_style))
    story.append(Paragraph("[4] Talreja, S., \"Beyond Generative Overhead in Agentic Tokenomics,\" 2026.", ref_style))

    doc.build(story, canvasmaker=IEEENumberedCanvas)
    print(f"[+] Successfully built IEEE Laya PDF at: {pdf_filename}")


if __name__ == "__main__":
    build_ieee_laya_pdf()
