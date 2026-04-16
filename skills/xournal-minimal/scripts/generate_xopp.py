#!/usr/bin/env python3
"""
generate_xopp.py — Erzeugt eine Xournal++ Datei (.xopp) für den Unterricht.

Eingabe: Eine JSON-Datei mit der Unterrichtsplanung.
Ausgabe: Eine .xopp-Datei im Template-Stil von Dr. Winkelmann.

Features:
- Automatischer Seitenumbruch bei Überlauf
- Saubere Margin-Begrenzung (kein Element ragt über Seitenrand)
- Proportionale Bildskalierung mit Crop-Unterstützung
"""

import json
import gzip
import base64
import sys
import os
import io
from xml.sax.saxutils import escape as xml_escape

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ─── Template-Konstanten ───────────────────────────────────────────────
PAGE_W = 595.27559
PAGE_H = 841.88976

# Ränder: nichts darf außerhalb dieses Bereichs liegen
MARGIN_LEFT = 14.17
MARGIN_RIGHT = 580.97
MARGIN_BOTTOM = 825.0  # Unterer Seitenrand (ca. 17pt Abstand)

# Nutzbarer Inhaltsbereich
CONTENT_LEFT = 16.37
CONTENT_RIGHT = 570.0   # 10pt Abstand zu MARGIN_RIGHT
CONTENT_WIDTH = CONTENT_RIGHT - CONTENT_LEFT  # ~553.6

# Header-Box (Phasenname links)
HEADER_BOX_LEFT = MARGIN_LEFT
HEADER_BOX_TOP = 14.17
HEADER_BOX_BOTTOM = 28.34
HEADER_BOX_BOTTOM_2LINE = 40.0   # Höhere Box für zweizeilige Kopfzeile
HEADER_BOX_RIGHT = 481.78

# Dr. Winkelmann Box (rechts oben)
DW_BOX_LEFT = 495.95
DW_BOX_TOP = 14.17
DW_BOX_BOTTOM = 28.34
DW_BOX_RIGHT = MARGIN_RIGHT

# Phasen-Subheader-Box (Einstieg-Seite)
PHASE_BOX_TOP = 42.51
PHASE_BOX_BOTTOM = 56.68

# Text-Positionen
TEXT_HEADER_X = 17.20
TEXT_HEADER_Y = 14.61
TEXT_DW_X = 496.97
TEXT_DW_Y = 15.34

# Y-Startpositionen
Y_START_AFTER_SIMPLE_HEADER = 38.0
Y_START_AFTER_DOUBLE_HEADER = 65.0

FONT = "Sans"
SIZE_NORMAL = 12
SIZE_LARGE = 14
SIZE_SMALL = 10
LINE_HEIGHT_FACTOR = 1.35  # Zeilenhöhe = Schriftgröße * Faktor

PEN_COLOR = "#000000ff"
BLUE_COLOR = "#3333ccff"
RED_COLOR = "#cc0000ff"
GRAY_COLOR = "#808080ff"

# Abstände
SPACING_AFTER_ELEMENT = 8
SPACING_AFTER_IMAGE = 10
SPACING_AFTER_FREIRAUM = 10


# ─── XML-Bausteine ────────────────────────────────────────────────────

def xml_header():
    return ('<?xml version="1.0" standalone="no"?>\n'
            '<xournal creator="xournalpp 1.2.7" fileversion="4">\n'
            '<title>Xournal++ document - see https://xournalpp.github.io/</title>\n')

def xml_footer():
    return '</xournal>\n'

def stroke_rect(left, top, right, bottom, width="0.77205084", color=PEN_COLOR):
    coords = f"{left} {top} {left} {bottom} {right} {bottom} {right} {top} {left} {top}"
    return f'<stroke tool="pen" color="{color}" width="{width}" capStyle="round">{coords}</stroke>\n'

def stroke_line(x1, y1, x2, y2, width="0.5", color=PEN_COLOR):
    return f'<stroke tool="pen" color="{color}" width="{width}" capStyle="round">{x1} {y1} {x2} {y2}</stroke>\n'

def text_element(x, y, text, font=FONT, size=SIZE_NORMAL, color=PEN_COLOR):
    escaped = xml_escape(str(text))
    return f'<text font="{font}" size="{size}" x="{x}" y="{y}" color="{color}">{escaped}</text>\n'

def image_element(left, top, right, bottom, base64_data):
    return f'<image left="{left}" top="{top}" right="{right}" bottom="{bottom}">{base64_data}</image>\n'


# ─── Hilfs-Funktionen ─────────────────────────────────────────────────

def wrap_text(text, max_chars=82):
    """Bricht Text um und gibt (wrapped_text, line_count) zurück."""
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            lines.append('')
            continue
        words = paragraph.split()
        current = ''
        for word in words:
            if len(current) + len(word) + 1 > max_chars:
                lines.append(current)
                current = word
            else:
                current = current + ' ' + word if current else word
        if current:
            lines.append(current)
    wrapped = '\n'.join(lines)
    return wrapped, len(lines)


def text_height(line_count, font_size=SIZE_NORMAL):
    """Berechnet die Höhe eines Textblocks."""
    return line_count * (font_size * LINE_HEIGHT_FACTOR)


def load_image_base64(filepath, crop=None):
    """Lädt ein Bild, schneidet optional zu.
    
    crop: dict mit Pixelkoordinaten ODER Prozentwerten:
        Pixel: {"left_px": 100, "top_px": 50, "right_px": 800, "bottom_px": 400}
        Prozent: {"left": 5, "top": 10, "right": 50, "bottom": 40}
    
    Gibt zurück: (base64_string, pixel_width, pixel_height)
    """
    if not HAS_PIL:
        with open(filepath, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('ascii')
        return b64, None, None

    img = Image.open(filepath)
    w, h = img.size

    if crop:
        # Pixel-Koordinaten haben Vorrang
        if "left_px" in crop:
            left   = int(crop.get("left_px", 0))
            top    = int(crop.get("top_px", 0))
            right  = int(crop.get("right_px", w))
            bottom = int(crop.get("bottom_px", h))
        else:
            # Prozent-Koordinaten
            left   = int(w * crop.get("left", 0) / 100)
            top    = int(h * crop.get("top", 0) / 100)
            right  = int(w * crop.get("right", 100) / 100)
            bottom = int(h * crop.get("bottom", 100) / 100)

        # Clamp
        left   = max(0, min(left, w - 1))
        top    = max(0, min(top, h - 1))
        right  = max(left + 1, min(right, w))
        bottom = max(top + 1, min(bottom, h))

        img = img.crop((left, top, right, bottom))

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return b64, img.size[0], img.size[1]


# ─── Header-Generatoren ───────────────────────────────────────────────

def make_page1_header(kopfzeile):
    """kopfzeile ist ein Tuple (zeile1, zeile2) für zweizeiligen Header."""
    line1, line2 = kopfzeile
    e = ""
    e += stroke_rect(HEADER_BOX_LEFT, HEADER_BOX_TOP, HEADER_BOX_RIGHT, HEADER_BOX_BOTTOM_2LINE)
    e += stroke_rect(DW_BOX_LEFT, DW_BOX_TOP, DW_BOX_RIGHT, DW_BOX_BOTTOM, width="0.85")
    e += text_element(TEXT_DW_X, TEXT_DW_Y, "Dr. Winkelmann")
    e += text_element(TEXT_HEADER_X, TEXT_HEADER_Y, line1)
    e += text_element(TEXT_HEADER_X, 27.0, line2)
    return e

def make_einstieg_header(phase_name, kopfzeile):
    """kopfzeile ist ein Tuple (zeile1, zeile2) für zweizeiligen Header."""
    line1, line2 = kopfzeile
    e = ""
    e += stroke_rect(HEADER_BOX_LEFT, HEADER_BOX_TOP, HEADER_BOX_RIGHT, HEADER_BOX_BOTTOM_2LINE)
    e += stroke_rect(DW_BOX_LEFT, DW_BOX_TOP, DW_BOX_RIGHT, DW_BOX_BOTTOM, width="0.85")
    e += text_element(TEXT_DW_X, TEXT_DW_Y, "Dr. Winkelmann")
    e += text_element(TEXT_HEADER_X, TEXT_HEADER_Y, line1)
    e += text_element(TEXT_HEADER_X, 27.0, line2)
    e += stroke_rect(MARGIN_LEFT, PHASE_BOX_TOP, MARGIN_RIGHT, PHASE_BOX_BOTTOM, width="0.85")
    e += text_element(16.85, 43.68, phase_name + ":")
    return e

def make_simple_header(phase_name):
    e = ""
    e += stroke_rect(HEADER_BOX_LEFT, HEADER_BOX_TOP, HEADER_BOX_RIGHT, HEADER_BOX_BOTTOM)
    e += stroke_rect(DW_BOX_LEFT, DW_BOX_TOP, DW_BOX_RIGHT, DW_BOX_BOTTOM, width="0.85")
    e += text_element(TEXT_DW_X, TEXT_DW_Y, "Dr. Winkelmann")
    e += text_element(17.76, 14.26, phase_name)
    return e

def make_page(layer_content):
    return (f'<page width="{PAGE_W}" height="{PAGE_H}">\n'
            f'<background type="solid" color="#ffffffff" style="graph"/>\n'
            f'<layer>\n{layer_content}</layer>\n</page>\n')


# ─── Vorlagen-Generatoren ─────────────────────────────────────────────

def make_koordinatensystem(cx, cy, width, height, x_label="x", y_label="y",
                           x_min=-5, x_max=5, y_min=-5, y_max=5):
    max_w = CONTENT_RIGHT - cx
    if width > max_w:
        width = max_w

    elements = ""
    elements += stroke_rect(cx, cy, cx + width, cy + height, width="0.3", color=GRAY_COLOR)

    x_range = x_max - x_min
    y_range = y_max - y_min
    if x_range == 0 or y_range == 0:
        return elements
    origin_x = cx + width * (-x_min / x_range)
    origin_y = cy + height * (y_max / y_range)

    elements += stroke_line(cx, origin_y, cx + width, origin_y, width="0.8")
    elements += stroke_line(origin_x, cy, origin_x, cy + height, width="0.8")
    elements += stroke_line(cx + width - 5, origin_y - 3, cx + width, origin_y, width="0.6")
    elements += stroke_line(cx + width - 5, origin_y + 3, cx + width, origin_y, width="0.6")
    elements += stroke_line(origin_x - 3, cy + 5, origin_x, cy, width="0.6")
    elements += stroke_line(origin_x + 3, cy + 5, origin_x, cy, width="0.6")
    elements += text_element(cx + width - 8, origin_y + 4, x_label, size=10)
    elements += text_element(origin_x + 4, cy, y_label, size=10)

    for i in range(int(x_min), int(x_max) + 1):
        if i == 0:
            continue
        px = cx + width * ((i - x_min) / x_range)
        elements += stroke_line(px, origin_y - 2, px, origin_y + 2, width="0.4")
        elements += text_element(px - 3, origin_y + 4, str(i), size=8, color=GRAY_COLOR)

    for j in range(int(y_min), int(y_max) + 1):
        if j == 0:
            continue
        py = cy + height * ((y_max - j) / y_range)
        elements += stroke_line(origin_x - 2, py, origin_x + 2, py, width="0.4")
        elements += text_element(origin_x - 14, py - 4, str(j), size=8, color=GRAY_COLOR)

    return elements


def make_table(x, y, rows, cols, col_width=80, row_height=22, headers=None):
    total_w = cols * col_width
    max_w = CONTENT_RIGHT - x
    if total_w > max_w:
        col_width = max_w / cols
        total_w = max_w
    total_h = rows * row_height

    elements = ""
    elements += stroke_rect(x, y, x + total_w, y + total_h, width="0.6")

    for r in range(1, rows):
        ry = y + r * row_height
        w = "0.6" if r == 1 and headers else "0.3"
        elements += stroke_line(x, ry, x + total_w, ry, width=w)

    for c in range(1, cols):
        cx_ = x + c * col_width
        elements += stroke_line(cx_, y, cx_, y + total_h, width="0.3")

    if headers:
        for i, h in enumerate(headers):
            elements += text_element(x + i * col_width + 3, y + 2, h, size=9, color=BLUE_COLOR)

    return elements, total_h


# ─── Seitenumbruch-fähiger Renderer ──────────────────────────────────

class PageRenderer:
    """Rendert Inhalte auf Seiten mit automatischem Umbruch."""

    def __init__(self, phase_name, kopfzeile, is_einstieg=False):
        self.phase_name = phase_name
        self.kopfzeile = kopfzeile
        self.is_einstieg = is_einstieg
        self.pages = []
        self.content = ""
        self.y = 0
        self._start_new_page(first=True)

    def _start_new_page(self, first=False):
        if self.content:
            self.pages.append(make_page(self.content))
            self.content = ""

        if first and self.is_einstieg:
            self.content = make_einstieg_header(self.phase_name, self.kopfzeile)
            self.y = Y_START_AFTER_DOUBLE_HEADER
        elif first:
            self.content = make_simple_header(self.phase_name + ":")
            self.y = Y_START_AFTER_SIMPLE_HEADER
        else:
            self.content = make_simple_header(self.phase_name + " (Forts.):")
            self.y = Y_START_AFTER_SIMPLE_HEADER

    def remaining(self):
        return MARGIN_BOTTOM - self.y

    def ensure_space(self, needed):
        if self.remaining() < needed:
            self._start_new_page()

    def add_text(self, text_str, font_size=SIZE_NORMAL, color=PEN_COLOR):
        wrapped, line_count = wrap_text(text_str)
        h = text_height(line_count, font_size)
        self.ensure_space(h + SPACING_AFTER_ELEMENT)
        self.content += text_element(CONTENT_LEFT, self.y, wrapped, size=font_size, color=color)
        self.y += h + SPACING_AFTER_ELEMENT

    def add_aufgabe(self, nr, text_str):
        wrapped, line_count = wrap_text(text_str)
        h = text_height(line_count, SIZE_NORMAL)
        self.ensure_space(h + SPACING_AFTER_ELEMENT)
        self.content += text_element(CONTENT_LEFT, self.y,
                                     f"{nr}) {wrapped}", size=SIZE_NORMAL, color=BLUE_COLOR)
        self.y += h + SPACING_AFTER_ELEMENT

    def add_merksatz(self, text_str):
        wrapped, line_count = wrap_text(text_str, max_chars=76)
        h = text_height(line_count, SIZE_NORMAL) + 24
        self.ensure_space(h + SPACING_AFTER_ELEMENT)
        box_top = self.y
        box_bottom = self.y + h
        box_right = min(CONTENT_RIGHT, MARGIN_RIGHT - 10)
        self.content += stroke_rect(CONTENT_LEFT, box_top, box_right, box_bottom,
                                    width="1.0", color=BLUE_COLOR)
        self.content += text_element(CONTENT_LEFT + 8, box_top + 4, "Merke:",
                                     size=SIZE_LARGE, color=BLUE_COLOR)
        self.content += text_element(CONTENT_LEFT + 8, box_top + 22, wrapped,
                                     size=SIZE_NORMAL, color=BLUE_COLOR)
        self.y = box_bottom + SPACING_AFTER_ELEMENT

    def add_freiraum(self, hoehe=150, label=""):
        label_h = 14 if label else 0
        total = label_h + hoehe
        self.ensure_space(min(total, 80))

        if label:
            self.content += text_element(CONTENT_LEFT, self.y, label,
                                         size=SIZE_SMALL, color=GRAY_COLOR)
            self.y += label_h

        actual_h = min(hoehe, self.remaining() - 5)
        actual_h = max(actual_h, 40)
        box_right = min(CONTENT_RIGHT, MARGIN_RIGHT - 10)
        self.content += stroke_rect(CONTENT_LEFT, self.y, box_right,
                                    self.y + actual_h, width="0.3", color=GRAY_COLOR)
        self.y += actual_h + SPACING_AFTER_FREIRAUM

    def add_koordinatensystem(self, width=250, height=200, x_label="x", y_label="y",
                               x_min=-5, x_max=5, y_min=-5, y_max=5):
        w = min(width, CONTENT_WIDTH - 40)
        h = min(height, 350)
        self.ensure_space(h + 20)
        cx = CONTENT_LEFT + 20
        self.content += make_koordinatensystem(cx, self.y, w, h,
                                               x_label, y_label,
                                               x_min, x_max, y_min, y_max)
        self.y += h + 15

    def add_tabelle(self, rows=5, cols=4, col_width=80, row_height=22, headers=None):
        max_w = CONTENT_WIDTH - 20
        if cols * col_width > max_w:
            col_width = max_w / cols
        total_h = rows * row_height
        self.ensure_space(total_h + 15)
        tbl_xml, tbl_h = make_table(CONTENT_LEFT + 10, self.y,
                                     rows, cols, col_width, row_height, headers)
        self.content += tbl_xml
        self.y += tbl_h + 15

    def add_bild(self, img_path, crop=None, display_width=None, buchseite=None):
        if not img_path or not os.path.exists(img_path):
            return

        # Buchseite-Referenz über dem Bild anzeigen
        if buchseite:
            ref_text = f"(Buch {buchseite})"
            self.ensure_space(20)
            self.content += text_element(CONTENT_LEFT, self.y, ref_text,
                                         size=SIZE_SMALL, color=GRAY_COLOR)
            self.y += 14

        b64, px_w, px_h = load_image_base64(img_path, crop=crop)

        if px_w and px_h:
            aspect = px_h / px_w
            if display_width:
                w = min(display_width, CONTENT_WIDTH)
            else:
                w = min(CONTENT_WIDTH, max(200, px_w * 0.45))
            h = w * aspect

            # Maximalhöhe begrenzen
            max_h = min(500, MARGIN_BOTTOM - Y_START_AFTER_SIMPLE_HEADER - 20)
            if h > max_h:
                h = max_h
                w = h / aspect
        else:
            w = display_width or 400
            h = 250

        self.ensure_space(min(h + SPACING_AFTER_IMAGE, 80))
        available = self.remaining() - 10
        if h > available:
            h = max(available, 50)
            if px_w and px_h:
                w = h / (px_h / px_w)

        left = CONTENT_LEFT + 5
        if left + w > CONTENT_RIGHT:
            w = CONTENT_RIGHT - left

        self.content += image_element(left, self.y, left + w, self.y + h, b64)
        self.y += h + SPACING_AFTER_IMAGE

    def add_linie(self):
        self.ensure_space(12)
        self.content += stroke_line(CONTENT_LEFT, self.y, CONTENT_RIGHT, self.y,
                                    width="0.4", color=GRAY_COLOR)
        self.y += 8

    def finalize(self):
        if self.content:
            self.pages.append(make_page(self.content))
        return ''.join(self.pages)


# ─── Hauptfunktionen ──────────────────────────────────────────────────

def build_page1(plan, kopfzeile):
    content = make_page1_header(kopfzeile)
    text = f"Vorbereitung für Lehrer:\n\n{plan.get('vorbereitung', '')}"
    wrapped, _ = wrap_text(text)
    content += text_element(CONTENT_LEFT, 48.0, wrapped, size=SIZE_NORMAL)
    return make_page(content)


def build_phase_pages(phase, kopfzeile, force_einstieg=None):
    phase_name = phase.get("name", "Phase")
    inhalte = phase.get("inhalte", [])
    if force_einstieg is not None:
        is_einstieg = force_einstieg
    else:
        is_einstieg = phase_name == "Einstieg"

    renderer = PageRenderer(phase_name, kopfzeile, is_einstieg=is_einstieg)

    for item in inhalte:
        t = item.get("type", "text")

        if t == "text":
            renderer.add_text(item.get("content", ""),
                              font_size=item.get("size", SIZE_NORMAL),
                              color=item.get("color", PEN_COLOR))
        elif t == "aufgabe":
            renderer.add_aufgabe(item.get("nr", ""), item.get("content", ""))
        elif t == "merksatz":
            renderer.add_merksatz(item.get("content", ""))
        elif t == "freiraum":
            renderer.add_freiraum(item.get("hoehe", 150), item.get("label", ""))
        elif t == "koordinatensystem":
            renderer.add_koordinatensystem(
                width=item.get("width", 250), height=item.get("height", 200),
                x_label=item.get("x_label", "x"), y_label=item.get("y_label", "y"),
                x_min=item.get("x_min", -5), x_max=item.get("x_max", 5),
                y_min=item.get("y_min", -5), y_max=item.get("y_max", 5))
        elif t == "tabelle":
            renderer.add_tabelle(
                rows=item.get("rows", 5), cols=item.get("cols", 4),
                col_width=item.get("col_width", 80), row_height=item.get("row_height", 22),
                headers=item.get("headers", None))
        elif t == "bild":
            renderer.add_bild(item.get("path", ""),
                              crop=item.get("crop", None),
                              display_width=item.get("width", None),
                              buchseite=item.get("buchseite", None))
        elif t == "linie":
            renderer.add_linie()

    return renderer.finalize()


def build_loesungen_pages(loesungen, kopfzeile):
    if isinstance(loesungen, str):
        loesungen = [{"type": "text", "content": loesungen}]

    renderer = PageRenderer("Lösungen und Hinweise - Nur für die Lehrkraft",
                            kopfzeile, is_einstieg=False)
    for item in loesungen:
        renderer.add_text(item.get("content", ""), font_size=SIZE_NORMAL)
    return renderer.finalize()


def generate_xopp(plan_path, output_path, image_paths=None):
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    fach = plan.get("fach", "Mathematik")
    sequenz = plan.get("sequenzthema", "")
    stunde = plan.get("stundenthema", "")
    # Zweizeiliger Header: Zeile 1 = Fach + Sequenz, Zeile 2 = Stundenthema
    kopfzeile = (f"{fach} - {sequenz}", stunde)

    xml = xml_header()

    if not plan.get("skip_vorbereitung", False):
        xml += build_page1(plan, kopfzeile)

    first_einstieg_done = False
    for phase in plan.get("phasen", []):
        phase_name = phase.get("name", "Phase")
        # Nur der allererste Einstieg bekommt den Doppel-Header
        is_einstieg = (phase_name == "Einstieg") and (not first_einstieg_done)
        if phase_name == "Einstieg":
            first_einstieg_done = True
        xml += build_phase_pages(phase, kopfzeile, force_einstieg=is_einstieg)

    if "loesungen" in plan and isinstance(plan["loesungen"], list):
        xml += build_loesungen_pages(plan["loesungen"], kopfzeile)

    xml += xml_footer()

    with gzip.open(output_path, 'wb') as f:
        f.write(xml.encode('utf-8'))

    page_count = xml.count('<page ')
    img_count = xml.count('<image ')
    print(f"✓ {output_path}: {page_count} Seiten, {img_count} Bilder")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python3 generate_xopp.py plan.json ausgabe.xopp")
        sys.exit(1)
    generate_xopp(sys.argv[1], sys.argv[2])
