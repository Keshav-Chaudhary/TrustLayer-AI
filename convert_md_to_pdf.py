import os
import sys
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute total page counts and render professional headers/footers.
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
        if self._pageNumber == 1:
            # Suppress header and footer on cover page
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Running Header
        self.drawString(54, 750, "TRUSTLAYER-AI — DEVELOPMENT & ENGINEERING REPORT")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)

        # Running Footer
        self.line(54, 48, 558, 48)
        self.setFont("Helvetica", 8)
        self.drawString(54, 34, "CONFIDENTIAL & PROPRIETARY — ACADEMIC RESEARCH & ENGINEERING REPORT")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_str)
        self.restoreState()


def format_markdown_text(text):
    """Clean and convert markdown text formatting safely to XML tags."""
    # Escape XML entity characters
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Format bold **text** safely
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    # Format italic *text* safely
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

    # Format inline code `code` safely
    text = re.sub(r'`(.*?)`', r"<font name='Courier'>\1</font>", text)

    # Remove inline LaTeX $ delimiters for clean display
    text = text.replace("$", "")

    return text


def build_pdf(md_filepath, pdf_filepath):
    doc = SimpleDocTemplate(
        pdf_filepath,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    PRIMARY = colors.HexColor("#1A365D")   # Deep Navy
    SECONDARY = colors.HexColor("#2B6CB0") # Steel Blue
    TEXT_DARK = colors.HexColor("#2D3748") # Dark Slate
    BG_LIGHT = colors.HexColor("#F7FAFC")  # Off-white

    # Custom Paragraph Styles
    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=PRIMARY,
        alignment=1, # Center
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name='DocSubtitle',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=SECONDARY,
        alignment=1,
        spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        name='CoverMeta',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=TEXT_DARK,
        alignment=1,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name='Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='Heading3_Custom',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=TEXT_DARK,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='Body_Custom',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='Bullet_Custom',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='Code_Custom',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C"),
        backColor=colors.HexColor("#EDF2F7"),
        borderColor=colors.HexColor("#CBD5E0"),
        borderWidth=0.5,
        borderPadding=5,
        spaceBefore=4,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    ))

    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=TEXT_DARK
    ))

    story = []

    with open(md_filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_cover = True
    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []

    for line in lines:
        raw_line = line
        line_str = line.strip()

        # Code block handling
        if line_str.startswith("```"):
            if in_code_block:
                code_text = "".join(code_lines)
                clean_code = code_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
                story.append(Paragraph(clean_code, styles['Code_Custom']))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(raw_line)
            continue

        # Table handling
        if "|" in line_str and line_str.startswith("|") and line_str.endswith("|"):
            if "---" in line_str:
                continue # Skip table divider row
            parts = [p.strip() for p in line_str.split("|")[1:-1]]
            if not in_table:
                in_table = True
                table_rows = [parts]
            else:
                table_rows.append(parts)
            continue
        else:
            if in_table:
                # Render accumulated table
                if table_rows:
                    num_cols = len(table_rows[0])
                    col_width = 504.0 / num_cols
                    col_widths = [col_width] * num_cols

                    table_data = []
                    for row_idx, row in enumerate(table_rows):
                        formatted_row = []
                        for cell in row:
                            style = styles['TableHeader'] if row_idx == 0 else styles['TableCell']
                            clean_cell = format_markdown_text(cell)
                            formatted_row.append(Paragraph(clean_cell, style))
                        table_data.append(formatted_row)

                    t = Table(table_data, colWidths=col_widths)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
                        ('TOPPADDING', (0,0), (-1,-1), 3),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                    ]))
                    story.append(Spacer(1, 4))
                    story.append(t)
                    story.append(Spacer(1, 8))
                in_table = False
                table_rows = []

        if not line_str:
            continue

        # Horizontal Rule
        if line_str == "---":
            if in_cover:
                in_cover = False
                story.append(Spacer(1, 40))
                story.append(PageBreak())
            else:
                story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceBefore=8, spaceAfter=12))
            continue

        # Headings
        if line_str.startswith("# "):
            title_text = line_str[2:].strip()
            if in_cover:
                story.append(Spacer(1, 80))
                story.append(Paragraph(format_markdown_text(title_text), styles['DocTitle']))
            else:
                story.append(Spacer(1, 10))
                story.append(Paragraph(format_markdown_text(title_text), styles['Heading1_Custom']))
            continue

        if line_str.startswith("## "):
            h2_text = line_str[3:].strip()
            if in_cover:
                story.append(Paragraph(format_markdown_text(h2_text), styles['DocSubtitle']))
            else:
                story.append(Paragraph(format_markdown_text(h2_text), styles['Heading2_Custom']))
            continue

        if line_str.startswith("### "):
            h3_text = line_str[4:].strip()
            if in_cover:
                story.append(Paragraph(format_markdown_text(h3_text), styles['DocSubtitle']))
            else:
                story.append(Paragraph(format_markdown_text(h3_text), styles['Heading3_Custom']))
            continue

        if line_str.startswith("#### "):
            h4_text = line_str[5:].strip()
            story.append(Paragraph(format_markdown_text(h4_text), styles['Heading3_Custom']))
            continue

        # Cover metadata text formatting
        if in_cover:
            story.append(Paragraph(format_markdown_text(line_str), styles['CoverMeta']))
            continue

        # Bullet Points
        if line_str.startswith("- ") or line_str.startswith("* "):
            bullet_text = line_str[2:].strip()
            story.append(Paragraph(f"• {format_markdown_text(bullet_text)}", styles['Bullet_Custom']))
            continue

        # Standard Paragraph Text
        story.append(Paragraph(format_markdown_text(line_str), styles['Body_Custom']))

    # Flush remaining table if file ends with table
    if in_table and table_rows:
        num_cols = len(table_rows[0])
        col_width = 504.0 / num_cols
        t = Table(table_rows, colWidths=[col_width]*num_cols)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), PRIMARY),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ]))
        story.append(t)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {pdf_filepath}")

if __name__ == "__main__":
    md_path = r"d:\Side_Projects\0_Independent_Project\NewBackend_start\TRUSTLAYER_AI_DEVELOPMENT_JOURNEY.md"
    pdf_path = r"d:\Side_Projects\0_Independent_Project\NewBackend_start\TRUSTLAYER_AI_DEVELOPMENT_JOURNEY.pdf"
    build_pdf(md_path, pdf_path)
