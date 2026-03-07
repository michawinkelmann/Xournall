#!/usr/bin/env python3
"""
Build Xournal++ lesson file for:
  Mathe 8G – Mehrstufige Zufallsexperimente
  6.3 Sinnvoller Umgang mit Baumdiagrammen
"""

import base64, gzip, io, os, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT_DIR = "/home/user/Xournall/Mathe/8G/Mehrstufige Zufallsexperimente"
os.makedirs(OUT_DIR, exist_ok=True)

# ─── helper: render figure to base64 PNG ────────────────────────────
def fig_to_b64(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight",
                pad_inches=0.08, facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

# ═══════════════════════════════════════════════════════════════════
# IMAGE 1 – Einstieg: Verkürztes Baumdiagramm (dreifacher Würfelwurf,
#            genau zweimal eine 6) – Beispiel 1, S. 186
# ═══════════════════════════════════════════════════════════════════
def make_short_tree_example1():
    """Dreifacher Würfelwurf – nur die Pfade mit genau zweimal 6."""
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.set_xlim(-0.5, 8.0)
    ax.set_ylim(-1.5, 6.0)
    ax.axis("off")

    # Root
    root = (4, 5.5)
    ax.plot(*root, 'ko', ms=6)

    # Level 1: 6 or keine 6
    l1 = [(1.8, 4.0, "6"), (6.2, 4.0, "keine 6")]

    # Level 2 from "6": 6 or keine 6
    l2_from6 = [(0.6, 2.2, "6"), (3.0, 2.2, "keine 6")]
    # Level 2 from "keine 6": 6 or keine 6
    l2_fromk = [(4.8, 2.2, "6"), (7.2, 2.2, "keine 6")]

    # Level 3 – only paths leading to exactly two 6s
    # From (6,6) -> keine 6
    l3_66k = (0.6, 0.4, "keine 6")
    # From (6, keine 6) -> 6
    l3_6k6 = (3.0, 0.4, "6")
    # From (keine 6, 6) -> 6  -- wait, we need keine 6 path too
    # Actually from (keine 6, 6) we need "keine 6" for exactly two 6s? No:
    # (6,6,keine6), (6,keine6,6), (keine6,6,6) are the three paths
    l3_k66 = (4.8, 0.4, "keine 6")

    def draw_node(x, y, label, r=0.3):
        if label == "6":
            fc, ec = "#e8f0fe", "#1a73e8"
        else:
            fc, ec = "#f5f5f5", "#888888"
        # Use box for longer labels
        bbox = dict(boxstyle="round,pad=0.3", fc=fc, ec=ec, lw=1.3)
        ax.text(x, y, label, ha="center", va="center", fontsize=11,
                fontweight="bold", bbox=bbox)

    def draw_edge(x1, y1, x2, y2, label):
        ax.annotate("", xy=(x2, y2+0.35), xytext=(x1, y1-0.35),
                     arrowprops=dict(arrowstyle="-", color="#555", lw=1.1))
        mx, my = (x1+x2)/2, (y1+y2)/2
        # offset label to the left of midpoint
        ax.text(mx - 0.45, my + 0.1, label, fontsize=10,
                color="#c62828", fontweight="bold")

    # Draw Level 1
    for n in l1:
        draw_node(*n)
    draw_edge(root[0], root[1], l1[0][0], l1[0][1], "1/6")
    draw_edge(root[0], root[1], l1[1][0], l1[1][1], "5/6")

    # Draw Level 2
    for n in l2_from6:
        draw_node(*n)
    for n in l2_fromk:
        draw_node(*n)
    draw_edge(l1[0][0], l1[0][1], l2_from6[0][0], l2_from6[0][1], "1/6")
    draw_edge(l1[0][0], l1[0][1], l2_from6[1][0], l2_from6[1][1], "5/6")
    draw_edge(l1[1][0], l1[1][1], l2_fromk[0][0], l2_fromk[0][1], "1/6")
    draw_edge(l1[1][0], l1[1][1], l2_fromk[1][0], l2_fromk[1][1], "5/6")

    # Draw Level 3 – only relevant branches for "genau zweimal 6"
    draw_node(*l3_66k)
    draw_node(*l3_6k6)
    draw_node(*l3_k66)

    # From (6,6) -> only keine 6
    draw_edge(l2_from6[0][0], l2_from6[0][1], l3_66k[0], l3_66k[1], "5/6")
    # From (6, keine 6) -> only 6
    draw_edge(l2_from6[1][0], l2_from6[1][1], l3_6k6[0], l3_6k6[1], "1/6")
    # From (keine 6, 6) -> only keine 6
    draw_edge(l2_fromk[0][0], l2_fromk[0][1], l3_k66[0], l3_k66[1], "5/6")

    # Gray out the (keine 6, keine 6) branch at level 2 – no further needed
    ax.text(7.2, 1.2, "...", fontsize=14, ha="center", color="#ccc")

    # Stage labels
    ax.text(-0.4, 4.7, "1. Wurf", fontsize=10, fontstyle="italic", color="#555")
    ax.text(-0.4, 3.0, "2. Wurf", fontsize=10, fontstyle="italic", color="#555")
    ax.text(-0.4, 1.1, "3. Wurf", fontsize=10, fontstyle="italic", color="#555")

    # Result annotations
    ax.text(0.6, -0.4, "(6; 6; keine 6)", fontsize=9, ha="center", color="#1a73e8")
    ax.text(3.0, -0.4, "(6; keine 6; 6)", fontsize=9, ha="center", color="#1a73e8")
    ax.text(4.8, -0.4, "(keine 6; 6; keine 6)", fontsize=9, ha="center", color="#1a73e8")

    # Probability formula
    ax.text(0.0, -1.1,
        "P(genau zweimal 6) = 3 \u00b7 1/6 \u00b7 1/6 \u00b7 5/6 = 15/216 \u2248 6,9 %",
        fontsize=10, color="#333", fontweight="bold")

    fig.tight_layout()
    return fig_to_b64(fig)


# ═══════════════════════════════════════════════════════════════════
# IMAGE 2 – Gegenereignis: Basketball-Beispiel (S. 187)
# ═══════════════════════════════════════════════════════════════════
def make_basketball_gegenereignis():
    """Zwei Spiele, P(gewinnt)=0.7. E1=beide gewinnen, E2=Gegenereignis."""
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.set_xlim(-0.5, 7.0)
    ax.set_ylim(-0.5, 5.0)
    ax.axis("off")

    root = (3.25, 4.5)
    ax.plot(*root, 'ko', ms=6)

    l1 = [(1.2, 3.0, "g"), (5.3, 3.0, "v")]
    l2 = [(0.2, 1.2, "g"), (2.2, 1.2, "v"),
          (4.3, 1.2, "g"), (6.3, 1.2, "v")]

    def dn(x, y, label, highlight=False):
        if label == "g":
            fc, ec = ("#c8e6c9", "#388e3c") if not highlight else ("#fff9c4", "#f9a825")
            txt = "gewinnt (g)"
        else:
            fc, ec = ("#ffcdd2", "#c62828") if not highlight else ("#fff9c4", "#f9a825")
            txt = "verliert (v)"
        bbox = dict(boxstyle="round,pad=0.25", fc=fc, ec=ec, lw=1.3)
        ax.text(x, y, txt, ha="center", va="center", fontsize=10,
                fontweight="bold", bbox=bbox)

    def de(x1, y1, x2, y2, label):
        ax.annotate("", xy=(x2, y2+0.3), xytext=(x1, y1-0.3),
                     arrowprops=dict(arrowstyle="-", color="#555", lw=1.1))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx-0.35, my+0.1, label, fontsize=10, color="#c62828", fontweight="bold")

    for n in l1: dn(*n)
    for n in l2: dn(*n)

    de(root[0], root[1], l1[0][0], l1[0][1], "0,7")
    de(root[0], root[1], l1[1][0], l1[1][1], "0,3")
    de(l1[0][0], l1[0][1], l2[0][0], l2[0][1], "0,7")
    de(l1[0][0], l1[0][1], l2[1][0], l2[1][1], "0,3")
    de(l1[1][0], l1[1][1], l2[2][0], l2[2][1], "0,7")
    de(l1[1][0], l1[1][1], l2[3][0], l2[3][1], "0,3")

    ax.text(-0.4, 3.7, "1. Spiel", fontsize=10, fontstyle="italic", color="#555")
    ax.text(-0.4, 1.8, "2. Spiel", fontsize=10, fontstyle="italic", color="#555")

    # Highlight E1 path
    from matplotlib.patches import FancyBboxPatch
    rect = mpatches.FancyBboxPatch((-0.5, 0.7), 1.4, 0.9,
        boxstyle="round,pad=0.1", fc="#fff9c4", ec="#f9a825", lw=1.5, alpha=0.3)
    ax.add_patch(rect)
    ax.text(0.2, 0.3, "E\u2081", fontsize=10, color="#f9a825", fontweight="bold", ha="center")

    fig.tight_layout()
    return fig_to_b64(fig)


# ═══════════════════════════════════════════════════════════════════
# IMAGE 3 – Gegenereignis: Beispiel 2 – mindestens eine 6 (S. 188)
# Verkürzter Baum: dreimal KEINE 6
# ═══════════════════════════════════════════════════════════════════
def make_gegen_beispiel2():
    """Dreifacher Wurf – Gegenereignis: dreimal keine 6."""
    fig, ax = plt.subplots(figsize=(5.0, 4.5))
    ax.set_xlim(-0.5, 5.0)
    ax.set_ylim(-1.0, 5.5)
    ax.axis("off")

    root = (2.5, 5.0)
    ax.plot(*root, 'ko', ms=6)

    # Single path: keine 6 -> keine 6 -> keine 6
    nodes = [(2.5, 3.5, "keine 6"), (2.5, 2.0, "keine 6"), (2.5, 0.5, "keine 6")]

    for x, y, label in nodes:
        bbox = dict(boxstyle="round,pad=0.3", fc="#f5f5f5", ec="#888", lw=1.3)
        ax.text(x, y, label, ha="center", va="center", fontsize=11,
                fontweight="bold", bbox=bbox)

    # Edges
    def de(x1, y1, x2, y2, label):
        ax.annotate("", xy=(x2, y2+0.35), xytext=(x1, y1-0.35),
                     arrowprops=dict(arrowstyle="-", color="#555", lw=1.1))
        ax.text(x1+0.4, (y1+y2)/2 + 0.1, label, fontsize=10, color="#c62828", fontweight="bold")

    de(root[0], root[1], nodes[0][0], nodes[0][1], "5/6")
    de(nodes[0][0], nodes[0][1], nodes[1][0], nodes[1][1], "5/6")
    de(nodes[1][0], nodes[1][1], nodes[2][0], nodes[2][1], "5/6")

    # Also show dashed lines for the "6" branches (not drawn)
    for i, (x, y, _) in enumerate([(root[0], root[1], ""),
                                     (nodes[0][0], nodes[0][1], ""),
                                     (nodes[1][0], nodes[1][1], "")]):
        target_y = [nodes[0][1], nodes[1][1], nodes[2][1]][i]
        ax.annotate("", xy=(x+1.3, target_y+0.1), xytext=(x, y-0.35),
                     arrowprops=dict(arrowstyle="-", color="#ccc", lw=0.8, ls="--"))
        ax.text(x+0.9, (y + target_y)/2 - 0.1, "1/6", fontsize=9, color="#ccc")

    ax.text(-0.4, 4.2, "1. Wurf", fontsize=10, fontstyle="italic", color="#555")
    ax.text(-0.4, 2.7, "2. Wurf", fontsize=10, fontstyle="italic", color="#555")
    ax.text(-0.4, 1.2, "3. Wurf", fontsize=10, fontstyle="italic", color="#555")

    # Result
    ax.text(0.2, -0.5,
        u"P(\u0112) = 5/6 \u00b7 5/6 \u00b7 5/6 = 125/216 \u2248 58 %",
        fontsize=10, color="#333", fontweight="bold")

    fig.tight_layout()
    return fig_to_b64(fig)


# ═══════════════════════════════════════════════════════════════════
# IMAGE 4 – Leeres Baumdiagramm (3-stufig, zum Ausfüllen)
# ═══════════════════════════════════════════════════════════════════
def make_empty_tree_3stage():
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    ax.set_xlim(-0.5, 8.0)
    ax.set_ylim(-0.5, 5.5)
    ax.axis("off")

    root = (4, 5.0)
    ax.plot(*root, 'o', ms=8, mfc="#ddd", mec="#aaa")

    l1 = [(1.5, 3.5), (6.5, 3.5)]
    l2 = [(0.3, 2.0), (2.7, 2.0), (5.3, 2.0), (7.7, 2.0)]
    l3 = [(-0.2, 0.5), (0.8, 0.5), (2.2, 0.5), (3.2, 0.5),
          (4.8, 0.5), (5.8, 0.5), (7.2, 0.5), (8.2, 0.5)]

    def draw_empty(x, y, r=0.25):
        circle = plt.Circle((x, y), r, fill=False, ec="#aaa", lw=1.0, ls="--")
        ax.add_patch(circle)
        ax.text(x, y, "?", ha="center", va="center", fontsize=10, color="#bbb")

    def draw_edge(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2+0.25), xytext=(x1, y1-0.25),
                     arrowprops=dict(arrowstyle="-", color="#ccc", lw=0.8, ls="--"))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx-0.2, my+0.08, "___", fontsize=8, color="#ccc")

    for p in l1: draw_empty(*p)
    for p in l2: draw_empty(*p)
    for p in l3: draw_empty(*p)

    for p in l1: draw_edge(root[0], root[1], p[0], p[1])
    for i, p in enumerate(l2):
        parent = l1[0] if i < 2 else l1[1]
        draw_edge(parent[0], parent[1], p[0], p[1])
    for i, p in enumerate(l3):
        parent = l2[i // 2]
        draw_edge(parent[0], parent[1], p[0], p[1])

    ax.text(-0.4, 4.2, "1. Stufe", fontsize=10, fontstyle="italic", color="#999")
    ax.text(-0.4, 2.7, "2. Stufe", fontsize=10, fontstyle="italic", color="#999")
    ax.text(-0.4, 1.1, "3. Stufe", fontsize=10, fontstyle="italic", color="#999")

    fig.tight_layout()
    return fig_to_b64(fig)


# ═══════════════════════════════════════════════════════════════════
# IMAGE 5 – Leeres Baumdiagramm (2-stufig)
# ═══════════════════════════════════════════════════════════════════
def make_empty_tree_2stage():
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis("off")

    root = (3, 4.0)
    ax.plot(*root, 'o', ms=8, mfc="#ddd", mec="#aaa")

    l1 = [(1.2, 2.5), (4.8, 2.5)]
    l2 = [(0.2, 0.8), (2.2, 0.8), (3.8, 0.8), (5.8, 0.8)]

    def draw_empty(x, y, r=0.3):
        circle = plt.Circle((x, y), r, fill=False, ec="#aaa", lw=1.0, ls="--")
        ax.add_patch(circle)
        ax.text(x, y, "?", ha="center", va="center", fontsize=11, color="#bbb")

    def draw_edge(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2+0.3), xytext=(x1, y1-0.3),
                     arrowprops=dict(arrowstyle="-", color="#ccc", lw=0.8, ls="--"))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx-0.2, my+0.08, "___", fontsize=8, color="#ccc")

    for p in l1: draw_empty(*p)
    for p in l2: draw_empty(*p)

    for p in l1: draw_edge(root[0], root[1], p[0], p[1])
    for i, p in enumerate(l2):
        parent = l1[0] if i < 2 else l1[1]
        draw_edge(parent[0], parent[1], p[0], p[1])

    ax.text(-0.4, 3.2, "1. Stufe", fontsize=10, fontstyle="italic", color="#999")
    ax.text(-0.4, 1.4, "2. Stufe", fontsize=10, fontstyle="italic", color="#999")

    fig.tight_layout()
    return fig_to_b64(fig)


# ═══════════════════════════════════════════════════════════════════
# IMAGE 6 – NNIA-Kugeln Baumdiagramm (Aufgabe 3 Illustration)
# ═══════════════════════════════════════════════════════════════════
def make_nnia_tree():
    """4 Kugeln N,N,I,A – dreimal ziehen mit Zurücklegen."""
    fig, ax = plt.subplots(figsize=(5.5, 2.5))
    ax.set_xlim(-0.2, 5.5)
    ax.set_ylim(-0.2, 2.5)
    ax.axis("off")

    # Just show the 4 colored balls
    colors = ["#1a73e8", "#1a73e8", "#e53935", "#ff9800"]
    labels = ["N", "N", "I", "A"]
    for i, (c, l) in enumerate(zip(colors, labels)):
        circle = plt.Circle((1 + i * 1.2, 1.5), 0.4, fill=True, fc=c, ec="#333", lw=1.5)
        ax.add_patch(circle)
        ax.text(1 + i * 1.2, 1.5, l, ha="center", va="center",
                fontsize=16, fontweight="bold", color="white")

    ax.text(2.8, 0.4, "4 Kugeln: N, N, I, A", fontsize=11, ha="center", color="#333")
    ax.text(2.8, 0.0, "P(N) = 2/4 = 1/2,  P(I) = 1/4,  P(A) = 1/4",
            fontsize=10, ha="center", color="#555")

    fig.tight_layout()
    return fig_to_b64(fig)


# ═══════════════════════════════════════════════════════════════════
# IMAGE 7 – Glücksrad für Aufgabe 6 (2 Farben-Bereiche)
# ═══════════════════════════════════════════════════════════════════
def make_gluecksrad():
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    # Simple pie chart as Glücksrad
    sizes = [50, 25, 25]
    colors_pie = ['#1a73e8', '#e53935', '#4caf50']
    labels_pie = ['Blau', 'Rot', 'Grün']
    wedges, texts = ax.pie(sizes, labels=labels_pie, colors=colors_pie,
                           startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    for t in texts:
        t.set_color("white")
    ax.set_aspect('equal')
    fig.tight_layout()
    return fig_to_b64(fig)


# ═══════════════════════════════════════════════════════════════════
# Generate all images
# ═══════════════════════════════════════════════════════════════════
print("Generating images...")
img_short_tree = make_short_tree_example1()
img_basketball_gegen = make_basketball_gegenereignis()
img_gegen_bsp2 = make_gegen_beispiel2()
img_empty_3stage = make_empty_tree_3stage()
img_empty_2stage = make_empty_tree_2stage()
img_nnia = make_nnia_tree()
img_gluecksrad = make_gluecksrad()
print("Images generated.")


# ═══════════════════════════════════════════════════════════════════
# Helper: page building blocks
# ═══════════════════════════════════════════════════════════════════
PAGE_W = "595.27559"
PAGE_H = "841.88976"

def page_start():
    return f'''<page width="{PAGE_W}" height="{PAGE_H}">
<background type="solid" color="#ffffffff" style="graph"/>
<layer>'''

def page_end():
    return "</layer>\n</page>"

HEADER_TITLE = "Mathe - Mehrstufige Zufallsexperimente: 6.3 Sinnvoller Umgang mit Baumdiagrammen"

def header_box(title=HEADER_TITLE):
    return f'''<stroke tool="pen" color="#000000ff" width="0.77205084" capStyle="round">14.17 28.34 14.17 14.17 481.78 14.17 481.78 28.34 14.17 28.34</stroke>
<text font="Sans" size="12" x="17.20" y="14.60" color="#000000ff">{title}</text>
<text font="Sans" size="12" x="496.97" y="15.34" color="#000000ff">Dr. Winkelmann</text>
<stroke tool="pen" color="#000000ff" width="0.85" capStyle="round">495.95 14.17 495.95 28.34 580.97 28.34 580.97 14.17 495.95 14.17</stroke>'''

def phase_box(label, y_top=42.51):
    y_bot = y_top + 14.17
    return f'''<text font="Sans" size="12" x="16.85" y="{y_top + 1.17}" color="#000000ff">{label}</text>
<stroke tool="pen" color="#000000ff" width="0.85" capStyle="round">14.17 {y_top} 14.17 {y_bot} 580.97 {y_bot} 580.97 {y_top} 14.17 {y_top}</stroke>'''

def text_block(x, y, text, size="11", color="#000000ff", font="Sans"):
    esc = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text font="{font}" size="{size}" x="{x}" y="{y}" color="{color}">{esc}</text>'

def image_tag(left, top, right, bottom, b64data):
    return f'<image left="{left}" top="{top}" right="{right}" bottom="{bottom}">{b64data}</image>'


# ═══════════════════════════════════════════════════════════════════
# BUILD PAGES
# ═══════════════════════════════════════════════════════════════════
pages = []

# ─── PAGE 1: Lehrerseite ──────────────────────────────────────────
p = page_start()
p += header_box()
p += text_block(16.37, 42.60, """Vorbereitung fuer Lehrkraft - NICHT fuer Schueler sichtbar

Lernziele / Kompetenzen:
- Die SuS erkennen, dass man nur die relevanten Teile
  eines Baumdiagramms zeichnen muss (verkuerzte
  Baumdiagramme).
- Die SuS kennen das Gegenereignis und koennen
  P(E) = 1 - P(Gegenereig.) anwenden.
- Die SuS entscheiden situationsabhaengig, ob ein
  direkter Weg oder der Umweg ueber das Gegenereignis
  einfacher ist.

Einordnung in die Sequenz:
- Vorwissen: 6.1 Baumdiagramme, 6.2 Pfadregeln
  (Multiplikation und Addition)
- Diese Stunde: Sinnvoller, effizienter Umgang mit
  Baumdiagrammen + Gegenereignis
- Ausblick: Anwendung auf komplexere Aufgaben

Verlaufsplan (90 Minuten):
Phase       | Inhalt                            | Zeit | Form
Einstieg    | Gluecksrad-Problem (10x10 Pfade?) | 8min | Plenum
Erarb. I    | Verkuerzte Baumdiagramme (Bsp.1)  |15min | PA
Sicherung I | Merksatz: nur relevante Pfade      | 5min | Plenum
Erarb. II   | Gegenereignis (Basketball, Bsp.2) |15min | PA
Sicherung II| Merksatz: P(E-quer) = 1 - P(E)    | 5min | Plenum
Uebung I    | Basisaufgaben S.186-188, Nr.1,2,5 |17min | EA
Uebung II   | Weiterfuehrend Nr.7, Nr.8         |15min | PA
Hausaufgabe | HA festlegen                       | 5min | Plenum
Puffer      | Reserve: Aufg. 10 (Lostrommel)     | 5min |

Material: Schulbuch S. 186-190, Beamer/Tablet

Didaktische Hinweise:
- Kernidee 1: Man muss NICHT immer alle Pfade
  zeichnen - nur die, die zum Ereignis gehoeren.
- Kernidee 2: Manchmal ist es einfacher, die W. des
  Gegenereignisses zu berechnen und von 1 abzuziehen.
- Typischer Fehler: Bei „mindestens eine 6" alle
  Pfade einzeln berechnen statt Gegenereignis nutzen.
- Differenzierung: Nr. 1-2,5 Basis; Nr. 7-8
  weiterfuehrend; Nr. 10-11 Challenge.

Diagnosefragen:
- „Wann lohnt es sich, nur einen Teil des
   Baumdiagramms zu zeichnen?"
- „Was ist das Gegenereignis zu ‚mindestens eine 6'?"

Reserve: Aufgabe 10 (Lostrommel, S.189)""", size="10")
p += page_end()
pages.append(p)

# ─── PAGE 2: Einstieg ─────────────────────────────────────────────
p = page_start()
p += header_box()
p += phase_box("Einstieg:")
p += text_block(16.37, 62.0, """Jana und Jonas stehen auf dem Schulfest beim
Gluecksrad. Wer beim zweimaligen Drehen zweimal
die 10 erhaelt, bekommt einen Preis.

Jonas sagt: „Um die Wahrscheinlichkeit fuer
einen Preis zu berechnen, muessen wir ein
Baumdiagramm zeichnen."

Jana meint: „Das geht nicht, es hat ja
10 x 10 Pfade."

Kannst du das Rechenproblem loesen?""", size="12")

p += text_block(16.37, 280, """Leitfrage: Muss man wirklich ALLE Pfade eines
Baumdiagramms zeichnen?""", size="12")

p += text_block(16.37, 340, """Ueberlege:
1) Welche Pfade sind fuer das Ereignis
   „zweimal die 10" relevant?
2) Genuegt es, nur diese Pfade zu zeichnen?
3) Wie viele Pfade brauchst du wirklich?""", size="11")

p += text_block(16.37, 500, "(Plenum, ca. 8 Minuten)", size="10", color="#999999ff")
p += page_end()
pages.append(p)

# ─── PAGE 3: Erarbeitung I – Verkürzte Baumdiagramme ─────────────
p = page_start()
p += header_box()
p += phase_box("Erarbeitung I: Verkuerzte Baumdiagramme")
p += text_block(16.37, 62.0, """Beispiel 1 (S. 186): Bestimme die Wahrscheinlichkeit,
mit der beim dreifachen Wurf mit einem Spielwuerfel
genau zweimal eine 6 gewuerfelt wird.

Loesung: Es genuegt, nur die Pfade zu zeichnen,
die zum Ereignis „genau zweimal 6" gehoeren.
Wir unterscheiden nur „6" und „keine 6".""", size="11")

p += image_tag(20, 200, 560, 530, img_short_tree)

p += text_block(16.37, 545, """Beobachtung:
- Man muss nur den Teil des Baumdiagramms zeichnen,
  der fuer das gesuchte Ereignis relevant ist.
- Drei Pfade fuehren zu „genau zweimal 6":
  (6;6;k6), (6;k6;6), (k6;6;6)
- Jeder Pfad hat die Wahrscheinlichkeit:
  1/6 * 1/6 * 5/6 = 5/216""", size="11")

p += text_block(16.37, 720, "(PA, ca. 15 Minuten – Besprechung S.186 lesen + Bsp. nachvollziehen)",
                size="10", color="#999999ff")
p += page_end()
pages.append(p)

# ─── PAGE 4: Sicherung I ─────────────────────────────────────────
p = page_start()
p += header_box()
p += phase_box("Sicherung I: Verkuerzte Baumdiagramme")
p += text_block(16.37, 70.0, """MERKSATZ - Sinnvoller Umgang mit Baumdiagrammen:

Moechte man die Wahrscheinlichkeit eines Ereignisses
bestimmen, genuegt es, nur den Teil des
Baumdiagramms mit den zugehoerigen Pfaden
zu zeichnen.

Man muss nicht alle moeglichen Ergebnisse
darstellen - nur die relevanten!""", size="12")

p += text_block(16.37, 240, """Vorgehensweise:
1. Ueberlege: Welche Ergebnisse gehoeren zum
   Ereignis?
2. Zeichne nur die Pfade, die zu diesen Ergebnissen
   fuehren.
3. Berechne die Wahrscheinlichkeit mit den
   Pfadregeln (Multiplikation + Addition).""", size="11")

p += text_block(16.37, 410, "(Platz fuer eigene Notizen und Beispiele)", size="10", color="#999999ff")
p += page_end()
pages.append(p)

# ─── PAGE 5: Erarbeitung II – Gegenereignis ──────────────────────
p = page_start()
p += header_box()
p += phase_box("Erarbeitung II: Wahrscheinlichkeit des Gegenereignisses")
p += text_block(16.37, 62.0, """Pascal ist Basketballfan. Sein Lieblingsteam
benoetigt in den naechsten beiden Spielen zwei
Siege. Er nimmt an, dass das Team jedes Spiel
mit einer Wahrscheinlichkeit von 70 % gewinnt.

E1: Das Team gewinnt beide Spiele.
E2: Das Team gewinnt hoechstens ein Spiel.

E2 ist das Gegenereignis zu E1.""", size="11")

p += image_tag(30, 230, 520, 490, img_basketball_gegen)

p += text_block(16.37, 505, """Aus dem Baumdiagramm:
P(E1) = 0,7 * 0,7 = 0,49 = 49 %

P(E2) = 0,7*0,3 + 0,3*0,7 + 0,3*0,3 = 0,51 = 51 %

Oder einfacher:
P(E2) = 1 - P(E1) = 1 - 0,49 = 0,51 = 51 %""", size="11")

p += text_block(16.37, 700, "(PA, ca. 15 Minuten – Text S.187 lesen + Zusammenhang erarbeiten)",
                size="10", color="#999999ff")
p += page_end()
pages.append(p)

# ─── PAGE 6: Sicherung II – Gegenereignis + Beispiel 2 ───────────
p = page_start()
p += header_box()
p += phase_box("Sicherung II: Gegenereignis")
p += text_block(16.37, 70.0, u"""MERKSATZ - Wahrscheinlichkeit des Gegenereignisses:

Das Gegenereignis \u0112 zu einem Ereignis E tritt
genau dann ein, wenn das Ereignis E NICHT eintritt.

Fuer seine Wahrscheinlichkeit gilt:
    P(\u0112) = 1 - P(E)""", size="12")

p += text_block(16.37, 210, """Beispiel 2 (S. 188): Bestimme die Wahrscheinlichkeit,
mit der beim dreifachen Wurf mit einem Spielwuerfel
mindestens eine 6 gewuerfelt wird.

Trick: Berechne zuerst das Gegenereignis
„dreimal KEINE 6" – das hat nur EINEN Pfad!""", size="11")

p += image_tag(80, 350, 420, 600, img_gegen_bsp2)

p += text_block(16.37, 620, u"""Gegenereignis \u0112: dreimal keine 6
P(\u0112) = 5/6 * 5/6 * 5/6 = 125/216 \u2248 58 %

Ereignis E: mindestens eine 6
P(E) = 1 - P(\u0112) = 1 - 125/216 = 91/216 \u2248 42 %""", size="12")
p += page_end()
pages.append(p)

# ─── PAGE 7: Übung I – Basisaufgaben ──────────────────────────────
p = page_start()
p += header_box()
p += phase_box(u"Uebung I - Basisaufgaben (EA, S.186/188):")
p += text_block(16.37, 62.0, """Aufgabe 1 (S. 186):
Bestimme die Wahrscheinlichkeit, dass man jedes Mal
eine Sechs erhaelt, wenn man viermal einen
Spielwuerfel wirft. Zeichne dazu nur den Teil eines
Baumdiagramms, der fuer die Bestimmung der
Wahrscheinlichkeit noetig ist.

Zeichne deinen verkürzten Baum hier:""", size="11")

p += text_block(16.37, 260, "(Platz fuer dein Baumdiagramm und Berechnung)",
                size="10", color="#999999ff")

p += text_block(16.37, 450, """Aufgabe 2 (S. 186):
Bei einem Quiz sollen fuenf gegebene Fluesse der
Laenge nach geordnet werden, vom kuerzesten bis zum
laengsten. Ermittle, mit welcher Wahrscheinlichkeit
ein ahnungsloser Kandidat, der die Fluesse rein
zufaellig ordnet, die richtige Reihenfolge raet.""", size="11")

p += text_block(16.37, 600, """Berechnung:""", size="11")

p += text_block(16.37, 750, "(EA, insgesamt ca. 17 Minuten fuer Aufg. 1, 2, 5)",
                size="10", color="#999999ff")
p += page_end()
pages.append(p)

# ─── PAGE 8: Übung I – Fortsetzung (Aufg. 5) ─────────────────────
p = page_start()
p += header_box()
p += phase_box(u"Uebung I - Fortsetzung (EA, S.188):")
p += text_block(16.37, 62.0, """Aufgabe 5 (S. 188):
Gib das Gegenereignis in Worten an.
a) Beim Werfen eines Spielwuerfels kommt eine
   gerade Augenzahl.
b) Aus einem Beutel mit farbigen Kugeln wird eine
   gelbe Kugel gezogen.
c) Eine zufaellige natuerliche Zahl zwischen 1
   und 49 ist kleiner als 20.
d) Bei der zufaelligen Auswahl zweier Schueler der
   Klasse 8a werden ein Maedchen und ein Junge
   gewaehlt.

Gegenereignisse:

a)

b)

c)

d)
""", size="11")

p += text_block(16.37, 500, """Fertig? Dann weiter mit Aufgabe 7 auf der
naechsten Seite!""", size="10", color="#999999ff")
p += page_end()
pages.append(p)

# ─── PAGE 9: Übung II – Weiterführend ────────────────────────────
p = page_start()
p += header_box()
p += phase_box(u"Uebung II - Weiterfuehrend (PA, S.188/189):")
p += text_block(16.37, 62.0, """Aufgabe 7 (S. 188):
Eine Muenze wird viermal geworfen. Bestimme die
Wahrscheinlichkeit, dass man mindestens einmal
Zahl erhaelt.

Tipp: Nutze das Gegenereignis!

Gegenereignis:


P(Gegenereignis) =


P(mindestens einmal Zahl) = 1 - P(Gegenereignis) =
""", size="11")

p += text_block(16.37, 370, """Aufgabe 8 (S. 189):
In einem Gefaess liegen drei rote, drei blaue und
drei weisse Kugeln. Viktoria zieht drei Kugeln
ohne Zuruecklegen. Berechne die Wahrscheinlichkeit,
dass sie
a) drei rote Kugeln,
b) mindestens eine rote Kugel zieht.

Hinweis zu b): Nutze das Gegenereignis
„keine rote Kugel"!

Berechnung:

a) P(3 rote) =



b) Gegenereignis: keine rote Kugel
   P(keine rote) =

   P(mindestens 1 rote) = 1 - P(keine rote) =
""", size="11")

p += text_block(16.37, 780, "(PA, ca. 15 Minuten)",
                size="10", color="#999999ff")
p += page_end()
pages.append(p)

# ─── PAGE 10: Hausaufgabe ─────────────────────────────────────────
p = page_start()
p += header_box()
p += phase_box("Hausaufgabe:")
p += text_block(16.37, 62.0, """Pflicht:
  Buch S. 188, Aufgabe 6
  (Gluecksrad zweimal drehen, Ereignis-Paare bilden,
   Wahrscheinlichkeiten berechnen)

Zusatz fuer Schnelle:
  Buch S. 189, Aufgabe 9
  (Handyakkus, 2 % defekt, Gegenereignis nutzen)""", size="12")

p += text_block(16.37, 220, """Aufgabe 6 (S. 188):
Das Gluecksrad wird zweimal gedreht und jeweils
die Farbe notiert.
a) Bilde aus den sechs Ereignissen drei Paare
   bestehend aus einem Ereignis und einem
   Gegenereignis.

   E1: zwei gleiche Farben
   E2: hoechstens einmal Rot
   E3: mindestens einmal Rot
   E4: nur Rot
   E5: nur Blau oder Gruen
   E6: zwei verschiedene Farben

b) Berechne die Wahrscheinlichkeiten der
   Ereignisse aus a).""", size="11")

p += text_block(16.37, 530, """Zuordnung der Paare (Ereignis + Gegenereignis):

Paar 1:    E___ und E___

Paar 2:    E___ und E___

Paar 3:    E___ und E___""", size="11")

p += page_end()
pages.append(p)

# ─── PAGE 11: Reserve ─────────────────────────────────────────────
p = page_start()
p += header_box()
p += phase_box("Reserve:")
p += text_block(16.37, 62.0, """Aufgabe 10 (S. 189):
In einer Lostrommel liegen 200 Lose, 50 davon
sind Gewinnlose. Nicole kauft 4 Lose.
Wie gross ist die Wahrscheinlichkeit fuer die
folgenden Ereignisse?
a) kein Gewinnlos
b) genau ein Gewinnlos
c) mindestens ein Gewinnlos

Hinweis: Vereinfacht mit Zuruecklegen rechnen
(grosse Grundgesamtheit).
P(Gewinn) = 50/200 = 1/4
P(kein Gewinn) = 3/4

Berechnung:

a) P(kein Gewinnlos) =



b) P(genau ein Gewinnlos) =



c) P(mindestens ein Gewinnlos) =
   Tipp: Nutze das Gegenereignis aus a)!
""", size="11")
p += page_end()
pages.append(p)

# ─── PAGE 12: Lösungen und Hinweise ──────────────────────────────
p = page_start()
p += header_box()
p += phase_box(u"Loesungen und Hinweise - Nur fuer die Lehrkraft:")
p += text_block(16.37, 65.0, u"""Einstieg - Gluecksrad:
Man braucht nur EINEN Pfad: (10; 10).
P(10; 10) = 1/10 * 1/10 = 1/100 = 1 %

Beispiel 1 - Genau zweimal 6 (dreifacher Wurf):
Drei Pfade: (6;6;k6), (6;k6;6), (k6;6;6)
Jeder: 1/6 * 1/6 * 5/6 = 5/216
P(genau 2x 6) = 3 * 5/216 = 15/216 \u2248 6,9 %

Beispiel 2 - Mindestens eine 6 (dreifacher Wurf):
Gegenereignis: dreimal keine 6
P(\u0112) = (5/6)^3 = 125/216
P(E) = 1 - 125/216 = 91/216 \u2248 42,1 %

Basketball:
P(E1) = 0,7 * 0,7 = 0,49 = 49 %
P(E2) = 1 - 0,49 = 0,51 = 51 %

Aufgabe 1:
P(viermal 6) = (1/6)^4 = 1/1296 \u2248 0,08 %

Aufgabe 2:
5 Fluesse in richtiger Reihenfolge:
P = 1/(5!) = 1/120 \u2248 0,83 %

Aufgabe 5 - Gegenereignisse:
a) eine ungerade Augenzahl
b) keine gelbe Kugel
c) Zahl ist >= 20 (also 20 bis 49)
d) zwei Maedchen oder zwei Jungen

Aufgabe 7:
Gegenereignis: viermal Kopf
P(4x Kopf) = (1/2)^4 = 1/16
P(mind. 1x Zahl) = 1 - 1/16 = 15/16 = 93,75 %""", size="10")
p += page_end()
pages.append(p)

# ─── PAGE 13: Lösungen Fortsetzung ────────────────────────────────
p = page_start()
p += header_box()
p += phase_box(u"Loesungen - Fortsetzung:")
p += text_block(16.37, 65.0, """Aufgabe 8:
a) P(3 rote) = 3/9 * 2/8 * 1/7 = 6/504 = 1/84
   (ohne Zuruecklegen!)

b) Gegenereignis: keine rote Kugel
   P(keine rote) = 6/9 * 5/8 * 4/7 = 120/504 = 5/21
   P(mind. 1 rote) = 1 - 5/21 = 16/21 = 76,2 %

Aufgabe 6 (Hausaufgabe):
Paare (Ereignis + Gegenereignis):
  E1 (zwei gleiche) und E6 (zwei verschiedene)
  E3 (mind. 1x Rot) und E5 (nur Blau oder Gruen)
  E2 (hoechstens 1x Rot) und E4 (nur Rot)
  Hinweis: E4 = „zweimal Rot", E2 = „nicht 2x Rot"

Wahrscheinlichkeiten haengen vom Gluecksrad ab
(Farbverteilung). Bei gleicher Verteilung
(je 1/3 Rot, Blau, Gruen):
  P(E1) = 3 * (1/3)^2 = 3/9 = 1/3
  P(E6) = 1 - 1/3 = 2/3
  P(E4) = (1/3)^2 = 1/9
  P(E2) = 1 - 1/9 = 8/9
  P(E3) = 1 - P(E5) = 1 - (2/3)^2 = 1 - 4/9 = 5/9
  P(E5) = 4/9

Aufgabe 9 (Zusatz):
P(defekt) = 0,02, P(ok) = 0,98
Vier Akkus: P(mind. 1 defekt) = 1 - 0,98^4
= 1 - 0,9224 = 0,0776 = 7,76 %

Aufgabe 10 (Reserve):
P(Gewinn) = 1/4, P(kein Gewinn) = 3/4
a) P(kein Gewinnlos) = (3/4)^4 = 81/256 = 31,6 %
b) P(genau 1) = 4 * (1/4) * (3/4)^3
   = 4 * 27/256 = 108/256 = 42,2 %
c) P(mind. 1) = 1 - 81/256 = 175/256 = 68,4 %

Typische Schuelerfehler:
- Alle Pfade zeichnen statt zu verkuerzen
- Gegenereignis falsch bestimmen (z.B. bei
  „mindestens eine 6": Gegenereignis ist
  „keine 6", NICHT „hoechstens eine 6")
- Vergessen, dass bei „ohne Zuruecklegen"
  sich die Wahrscheinlichkeiten aendern

Impulse:
- „Welche Pfade brauchst du NICHT?"
- „Was ist das Gegenteil von deinem Ereignis?"
- „Ist der Umweg ueber das Gegenereignis
   einfacher?"
""", size="10")
p += page_end()
pages.append(p)

# ═══════════════════════════════════════════════════════════════════
# ASSEMBLE XML AND WRITE GZIPPED .xopp
# ═══════════════════════════════════════════════════════════════════
xml = '<?xml version="1.0" standalone="no"?>\n'
xml += '<xournal creator="xournalpp 1.2.7" fileversion="4">\n'
xml += '<title>Xournal++ document - see https://xournalpp.github.io/</title>\n'
for p in pages:
    xml += p + "\n"
xml += "</xournal>\n"

out_path = os.path.join(OUT_DIR, "6.3 Sinnvoller Umgang mit Baumdiagrammen.xopp")
with gzip.open(out_path, "wb") as f:
    f.write(xml.encode("utf-8"))

print(f"Done! File saved to: {out_path}")
print(f"XML size: {len(xml)} bytes")
print(f"Pages: {len(pages)}")
