#!/usr/bin/env python3
"""
generate_loesungen_pdf.py — Erzeugt eine Lösungs-PDF für die Lehrkraft.

Eingabe: Eine JSON-Datei mit der Unterrichtsplanung (inkl. "loesungen"-Feld).
Ausgabe: Eine PDF-Datei mit allen Lösungen, gegliedert nach Phasen.

Benötigt: fpdf2 (pip install fpdf2)
"""

import json
import sys
import os

from fpdf import FPDF


class LoesungenPDF(FPDF):
    """PDF-Klasse mit Header/Footer für Lösungsblätter."""

    def __init__(self, fach, stundenthema):
        super().__init__()
        self.fach = fach
        self.stundenthema = stundenthema
        # DejaVu für Umlaute
        font_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts')
        dejavu = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        dejavu_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        dejavu_italic = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'

        if os.path.exists(dejavu):
            self.add_font('DejaVu', '', dejavu)
            self.add_font('DejaVu', 'B', dejavu_bold)
            italic_file = dejavu_italic if os.path.exists(dejavu_italic) else dejavu
            self.add_font('DejaVu', 'I', italic_file)
            self.default_font = 'DejaVu'
        else:
            self.default_font = 'Helvetica'

    def header(self):
        self.set_font(self.default_font, 'B', 10)
        self.cell(0, 6, f'{self.fach} — {self.stundenthema}', border='B', new_x='LMARGIN', new_y='NEXT')
        self.set_font(self.default_font, 'I', 8)
        self.cell(0, 5, 'Lösungen — Nur für die Lehrkraft', new_x='LMARGIN', new_y='NEXT')
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.default_font, 'I', 8)
        self.cell(0, 10, f'Dr. Winkelmann — Seite {self.page_no()}', align='R')


def generate_loesungen_pdf(plan_path, output_path):
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    fach = plan.get('fach', 'Mathematik')
    stundenthema = plan.get('stundenthema', '')
    loesungen = plan.get('loesungen', {})

    if not loesungen:
        print("⚠ Kein 'loesungen'-Feld im Plan gefunden. Keine PDF erzeugt.")
        return None

    pdf = LoesungenPDF(fach, stundenthema)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    font = pdf.default_font

    # Lösungen sind nach Phasen gegliedert
    if isinstance(loesungen, dict):
        for phase_name, items in loesungen.items():
            # Phasen-Überschrift
            pdf.set_font(font, 'B', 12)
            pdf.set_text_color(51, 51, 204)  # Blau
            pdf.cell(0, 8, phase_name, new_x='LMARGIN', new_y='NEXT')
            pdf.set_draw_color(51, 51, 204)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 180, pdf.get_y())
            pdf.ln(3)

            pdf.set_text_color(0, 0, 0)
            pdf.set_font(font, '', 10)

            if isinstance(items, list):
                for item in items:
                    _render_item(pdf, font, item)
            elif isinstance(items, str):
                pdf.multi_cell(0, 5, items)
                pdf.ln(3)

    elif isinstance(loesungen, list):
        pdf.set_font(font, '', 10)
        for item in loesungen:
            _render_item(pdf, font, item)

    elif isinstance(loesungen, str):
        pdf.set_font(font, '', 10)
        pdf.multi_cell(0, 5, loesungen)

    pdf.output(output_path)
    print(f"✓ {output_path}: Lösungs-PDF erzeugt ({pdf.page_no()} Seiten)")
    return output_path


def _render_item(pdf, font, item):
    """Rendert ein einzelnes Lösungs-Element."""
    if isinstance(item, str):
        pdf.multi_cell(0, 5, item)
        pdf.ln(2)
        return

    t = item.get('type', 'text')

    if t == 'ueberschrift':
        pdf.set_font(font, 'B', 11)
        pdf.set_text_color(51, 51, 204)
        pdf.cell(0, 7, item.get('content', ''), new_x='LMARGIN', new_y='NEXT')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font, '', 10)
        pdf.ln(1)

    elif t == 'aufgabe':
        nr = item.get('nr', '')
        pdf.set_font(font, 'B', 10)
        pdf.cell(0, 6, f"Aufgabe {nr}:", new_x='LMARGIN', new_y='NEXT')
        pdf.set_font(font, '', 10)
        loesung = item.get('loesung', '')
        if isinstance(loesung, list):
            for line in loesung:
                pdf.set_x(pdf.l_margin + 5)
                pdf.multi_cell(0, 5, str(line))
        else:
            pdf.set_x(pdf.l_margin + 5)
            pdf.multi_cell(0, 5, str(loesung))
        pdf.ln(2)

    elif t == 'text':
        content = item.get('content', '')
        bold = item.get('bold', False)
        pdf.set_font(font, 'B' if bold else '', 10)
        pdf.multi_cell(0, 5, content)
        pdf.set_font(font, '', 10)
        pdf.ln(2)

    elif t == 'tabelle':
        headers = item.get('headers', [])
        rows = item.get('rows', [])
        col_count = len(headers) if headers else (len(rows[0]) if rows else 0)
        if col_count == 0:
            return
        col_w = min(180 / col_count, 40)

        if headers:
            pdf.set_font(font, 'B', 9)
            for h in headers:
                pdf.cell(col_w, 6, str(h), border=1, align='C')
            pdf.ln()

        pdf.set_font(font, '', 9)
        for row in rows:
            for cell in row:
                pdf.cell(col_w, 6, str(cell), border=1, align='C')
            pdf.ln()
        pdf.ln(3)

    elif t == 'linie':
        pdf.set_draw_color(180, 180, 180)
        y = pdf.get_y()
        pdf.line(10, y, 200, y)
        pdf.set_draw_color(0, 0, 0)
        pdf.ln(3)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Verwendung: python3 generate_loesungen_pdf.py plan.json loesungen.pdf")
        sys.exit(1)
    generate_loesungen_pdf(sys.argv[1], sys.argv[2])
