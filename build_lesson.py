#!/usr/bin/env python3
"""
Build Xournal++ lesson file for:
  Mathe 8G – Mehrstufige Zufallsexperimente
  6.2 Wahrscheinlichkeiten bei Baumdiagrammen
"""

import base64, gzip, io, os, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

OUT_DIR = "/home/user/Xournall/Mathe/8G/Mehrstufige Zufallsexperimente"
IMG_DIR = "/tmp/xopp_imgs"
os.makedirs(IMG_DIR, exist_ok=True)

# ─── helper: render figure to base64 PNG ────────────────────────────
def fig_to_b64(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight",
                pad_inches=0.08, facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

# ═══════════════════════════════════════════════════════════════════
# IMAGE 1 – Einstieg: Münz-Baumdiagramm (zweifacher Münzwurf)
# ═══════════════════════════════════════════════════════════════════
def make_coin_tree():
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis("off")

    # Nodes: (x, y, label)
    root = (3, 4, "Start")
    l1 = [(1.2, 2.5, "K"), (4.8, 2.5, "Z")]
    l2 = [
        (0.2, 0.8, "K"), (2.2, 0.8, "Z"),
        (3.8, 0.8, "K"), (5.8, 0.8, "Z"),
    ]

    def draw_node(x, y, label, r=0.35):
        circle = plt.Circle((x, y), r, fill=True, fc="#e8f0fe", ec="#1a73e8", lw=1.5)
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center", fontsize=13, fontweight="bold")

    def draw_edge(x1, y1, x2, y2, label):
        ax.annotate("", xy=(x2, y2+0.35), xytext=(x1, y1-0.35),
                     arrowprops=dict(arrowstyle="-", color="#555", lw=1.2))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx-0.35, my+0.1, label, fontsize=11, color="#c62828", fontweight="bold")

    draw_node(*root)
    for n in l1:
        draw_node(*n)
    for n in l2:
        draw_node(*n)

    # Edges root→l1
    draw_edge(root[0], root[1], l1[0][0], l1[0][1], "½")
    draw_edge(root[0], root[1], l1[1][0], l1[1][1], "½")

    # Edges l1→l2
    draw_edge(l1[0][0], l1[0][1], l2[0][0], l2[0][1], "½")
    draw_edge(l1[0][0], l1[0][1], l2[1][0], l2[1][1], "½")
    draw_edge(l1[1][0], l1[1][1], l2[2][0], l2[2][1], "½")
    draw_edge(l1[1][0], l1[1][1], l2[3][0], l2[3][1], "½")

    # Stage labels
    ax.text(-0.4, 3.2, "1. Wurf", fontsize=11, fontstyle="italic", color="#555")
    ax.text(-0.4, 1.5, "2. Wurf", fontsize=11, fontstyle="italic", color="#555")

    fig.tight_layout()
    return fig_to_b64(fig)

# ═══════════════════════════════════════════════════════════════════
# IMAGE 2 – Ergebnistabelle Münzwurf
# ═══════════════════════════════════════════════════════════════════
def make_coin_table():
    fig, ax = plt.subplots(figsize=(5.5, 2.2))
    ax.axis("off")
    table_data = [
        ["Ergebnis", "Wahrscheinlichkeit"],
        ["(Kopf; Kopf)", "½ · ½ = ¼ = 25 %"],
        ["(Kopf; Zahl)", "½ · ½ = ¼ = 25 %"],
        ["(Zahl; Kopf)", "½ · ½ = ¼ = 25 %"],
        ["(Zahl; Zahl)", "½ · ½ = ¼ = 25 %"],
    ]
    colors = [["#1a73e8"]*2] + [["white"]*2]*4
    tbl = ax.table(cellText=table_data, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1.0, 1.6)
    for (r, c), cell in tbl.get_celld().items():
        if r == 0:
            cell.set_facecolor("#1a73e8")
            cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor("#f8f9fa" if r % 2 == 0 else "white")
        cell.set_edgecolor("#ddd")
    fig.tight_layout()
    return fig_to_b64(fig)

# ═══════════════════════════════════════════════════════════════════
# IMAGE 3 – Glücksrad Baumdiagramm (Rot/Blau, 2/3 und 1/3)
# ═══════════════════════════════════════════════════════════════════
def make_spinner_tree():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.5, 5.0)
    ax.axis("off")

    root = (3.5, 4.5, "Start")
    l1 = [(1.5, 2.8, "Rot"), (5.5, 2.8, "Blau")]
    l2 = [
        (0.3, 0.8, "Rot"), (2.7, 0.8, "Blau"),
        (4.3, 0.8, "Rot"), (6.7, 0.8, "Blau"),
    ]

    def draw_node(x, y, label, r=0.4):
        col = "#e53935" if "Rot" in label else ("#1e88e5" if "Blau" in label else "#e8f0fe")
        tc = "white" if label in ("Rot", "Blau") else "black"
        circle = plt.Circle((x, y), r, fill=True, fc=col, ec="#333", lw=1.5)
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center", fontsize=11, fontweight="bold", color=tc)

    def draw_edge(x1, y1, x2, y2, label):
        ax.annotate("", xy=(x2, y2+0.4), xytext=(x1, y1-0.4),
                     arrowprops=dict(arrowstyle="-", color="#555", lw=1.2))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx-0.3, my+0.1, label, fontsize=11, color="#c62828", fontweight="bold")

    draw_node(*root)
    for n in l1:
        draw_node(*n)
    for n in l2:
        draw_node(*n)

    draw_edge(root[0], root[1], l1[0][0], l1[0][1], "⅔")
    draw_edge(root[0], root[1], l1[1][0], l1[1][1], "⅓")
    draw_edge(l1[0][0], l1[0][1], l2[0][0], l2[0][1], "⅔")
    draw_edge(l1[0][0], l1[0][1], l2[1][0], l2[1][1], "⅓")
    draw_edge(l1[1][0], l1[1][1], l2[2][0], l2[2][1], "⅔")
    draw_edge(l1[1][0], l1[1][1], l2[3][0], l2[3][1], "⅓")

    ax.text(-0.4, 3.6, "1. Drehung", fontsize=11, fontstyle="italic", color="#555")
    ax.text(-0.4, 1.6, "2. Drehung", fontsize=11, fontstyle="italic", color="#555")

    # Result annotation
    ax.text(0.3, 0.0, "P(Rot; Rot) = ⅔ · ⅔ = 4/9", fontsize=10, color="#333")

    fig.tight_layout()
    return fig_to_b64(fig)

# ═══════════════════════════════════════════════════════════════════
# IMAGE 4 – Pfadadditionsregel Baum (zweifacher Münzwurf,
#            Markierung "einmal Kopf, einmal Zahl")
# ═══════════════════════════════════════════════════════════════════
def make_addition_tree():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-1.0, 5.5)
    ax.axis("off")

    root = (3.5, 5, "")
    l1 = [(1.5, 3.2, "K"), (5.5, 3.2, "Z")]
    l2 = [
        (0.3, 1.2, "K"), (2.7, 1.2, "Z"),
        (4.3, 1.2, "K"), (5.5, 1.2, "Z"),  # shifted for clarity
    ]
    # Fix: last node
    l2[3] = (6.7, 1.2, "Z")

    def draw_node(x, y, label, highlight=False, r=0.35):
        fc = "#fff9c4" if highlight else "#e8f0fe"
        ec = "#f9a825" if highlight else "#1a73e8"
        lw = 2.5 if highlight else 1.5
        circle = plt.Circle((x, y), r, fill=True, fc=fc, ec=ec, lw=lw)
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center", fontsize=13, fontweight="bold")

    def draw_edge(x1, y1, x2, y2, label, highlight=False):
        col = "#f9a825" if highlight else "#555"
        lw = 2.0 if highlight else 1.2
        ax.annotate("", xy=(x2, y2+0.35), xytext=(x1, y1-0.35),
                     arrowprops=dict(arrowstyle="-", color=col, lw=lw))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx-0.3, my+0.1, label, fontsize=11, color="#c62828", fontweight="bold")

    # Root
    ax.plot(root[0], root[1], 'ko', ms=6)

    for n in l1:
        draw_node(*n)
    # Highlight (K;Z) and (Z;K) paths
    draw_node(*l2[0])
    draw_node(*l2[1], highlight=True)   # K→Z
    draw_node(*l2[2], highlight=True)   # Z→K
    draw_node(*l2[3])

    draw_edge(root[0], root[1], l1[0][0], l1[0][1], "½")
    draw_edge(root[0], root[1], l1[1][0], l1[1][1], "½")

    draw_edge(l1[0][0], l1[0][1], l2[0][0], l2[0][1], "½")
    draw_edge(l1[0][0], l1[0][1], l2[1][0], l2[1][1], "½", highlight=True)
    draw_edge(l1[1][0], l1[1][1], l2[2][0], l2[2][1], "½", highlight=True)
    draw_edge(l1[1][0], l1[1][1], l2[3][0], l2[3][1], "½")

    ax.text(0.3, 1.2-0.6, "(K;K)", fontsize=9, ha="center", color="#888")
    ax.text(2.7, 1.2-0.6, "(K;Z)", fontsize=9, ha="center", color="#f9a825", fontweight="bold")
    ax.text(4.3, 1.2-0.6, "(Z;K)", fontsize=9, ha="center", color="#f9a825", fontweight="bold")
    ax.text(6.7, 1.2-0.6, "(Z;Z)", fontsize=9, ha="center", color="#888")

    ax.text(-0.3, 4.0, "1. Wurf", fontsize=11, fontstyle="italic", color="#555")
    ax.text(-0.3, 2.0, "2. Wurf", fontsize=11, fontstyle="italic", color="#555")

    # Formula
    ax.text(0.5, -0.5, 'P("einmal K, einmal Z") = P(K;Z) + P(Z;K) = ¼ + ¼ = ½',
            fontsize=10, color="#333", fontweight="bold")

    fig.tight_layout()
    return fig_to_b64(fig)

# ═══════════════════════════════════════════════════════════════════
# IMAGE 5 – Leeres Baumdiagramm-Template (2-stufig, zum Ausfüllen)
# ═══════════════════════════════════════════════════════════════════
def make_empty_tree():
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 5.0)
    ax.axis("off")

    root = (3, 4.5, "")
    l1_pos = [(1.2, 2.8), (4.8, 2.8)]
    l2_pos = [
        (0.2, 0.8), (2.2, 0.8),
        (3.8, 0.8), (5.8, 0.8),
    ]

    def draw_empty_node(x, y, r=0.35):
        circle = plt.Circle((x, y), r, fill=False, ec="#aaa", lw=1.2, ls="--")
        ax.add_patch(circle)
        ax.text(x, y, "?", ha="center", va="center", fontsize=12, color="#bbb")

    def draw_edge(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2+0.35), xytext=(x1, y1-0.35),
                     arrowprops=dict(arrowstyle="-", color="#ccc", lw=1.0, ls="--"))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx-0.25, my+0.1, "___", fontsize=9, color="#ccc")

    ax.plot(root[0], root[1], 'o', ms=8, mfc="#ddd", mec="#aaa")
    for pos in l1_pos:
        draw_empty_node(*pos)
    for pos in l2_pos:
        draw_empty_node(*pos)

    draw_edge(root[0], root[1], l1_pos[0][0], l1_pos[0][1])
    draw_edge(root[0], root[1], l1_pos[1][0], l1_pos[1][1])
    for i, l2 in enumerate(l2_pos):
        parent = l1_pos[0] if i < 2 else l1_pos[1]
        draw_edge(parent[0], parent[1], l2[0], l2[1])

    ax.text(-0.4, 3.6, "1. Stufe", fontsize=11, fontstyle="italic", color="#999")
    ax.text(-0.4, 1.5, "2. Stufe", fontsize=11, fontstyle="italic", color="#999")

    fig.tight_layout()
    return fig_to_b64(fig)

# ═══════════════════════════════════════════════════════════════════
# IMAGE 6 – Basketball-Baumdiagramm (Aufgabe 3)
# ═══════════════════════════════════════════════════════════════════
def make_basketball_tree():
    """3-stufig: P(Treffer)=0.6, P(kein Treffer)=0.4, drei Würfe"""
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-1.0, 6.0)
    ax.axis("off")

    root = (4, 5.5, "")
    ax.plot(root[0], root[1], 'ko', ms=6)

    # Level 1
    l1 = [(1.5, 4.0, "T"), (6.5, 4.0, "K")]
    # Level 2
    l2 = [(0.5, 2.3, "T"), (2.5, 2.3, "K"),
           (5.5, 2.3, "T"), (7.5, 2.3, "K")]
    # Level 3
    l3 = [(0.0, 0.5, "T"), (1.0, 0.5, "K"),
           (2.0, 0.5, "T"), (3.0, 0.5, "K"),
           (5.0, 0.5, "T"), (6.0, 0.5, "K"),
           (7.0, 0.5, "T"), (8.0, 0.5, "K")]

    def dn(x, y, label, r=0.3):
        fc = "#c8e6c9" if label == "T" else "#ffcdd2"
        ec = "#388e3c" if label == "T" else "#c62828"
        circle = plt.Circle((x, y), r, fill=True, fc=fc, ec=ec, lw=1.3)
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center", fontsize=10, fontweight="bold")

    def de(x1, y1, x2, y2, label, r=0.3):
        ax.annotate("", xy=(x2, y2+r), xytext=(x1, y1-r),
                     arrowprops=dict(arrowstyle="-", color="#555", lw=1.0))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx-0.25, my+0.05, label, fontsize=9, color="#c62828", fontweight="bold")

    for n in l1: dn(*n)
    for n in l2: dn(*n)
    for n in l3: dn(*n)

    de(root[0], root[1], l1[0][0], l1[0][1], "0,6")
    de(root[0], root[1], l1[1][0], l1[1][1], "0,4")

    for i, n2 in enumerate(l2):
        parent = l1[0] if i < 2 else l1[1]
        lbl = "0,6" if n2[2] == "T" else "0,4"
        de(parent[0], parent[1], n2[0], n2[1], lbl)

    for i, n3 in enumerate(l3):
        parent = l2[i // 2]
        lbl = "0,6" if n3[2] == "T" else "0,4"
        de(parent[0], parent[1], n3[0], n3[1], lbl)

    ax.text(-0.4, 4.7, "1. Wurf", fontsize=10, fontstyle="italic", color="#555")
    ax.text(-0.4, 3.0, "2. Wurf", fontsize=10, fontstyle="italic", color="#555")
    ax.text(-0.4, 1.2, "3. Wurf", fontsize=10, fontstyle="italic", color="#555")

    ax.text(0, -0.5, "T = Treffer (0,6)    K = kein Treffer (0,4)", fontsize=9, color="#555")

    fig.tight_layout()
    return fig_to_b64(fig)

# ═══════════════════════════════════════════════════════════════════
# IMAGE 7 – Tennisbälle Baumdiagramm (abhängige Stufen, Bsp 3)
# ═══════════════════════════════════════════════════════════════════
def make_tennis_tree():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.5, 5.0)
    ax.axis("off")

    root = (3.5, 4.5, "")
    ax.plot(root[0], root[1], 'ko', ms=6)

    l1 = [(1.5, 2.8, "g"), (5.5, 2.8, "n")]
    l2 = [(0.3, 0.8, "g"), (2.7, 0.8, "n"),
           (4.3, 0.8, "g"), (6.7, 0.8, "n")]

    def dn(x, y, label, r=0.35):
        fc = "#fff3e0" if label == "g" else "#e3f2fd"
        ec = "#e65100" if label == "g" else "#1565c0"
        circle = plt.Circle((x, y), r, fill=True, fc=fc, ec=ec, lw=1.5)
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center", fontsize=12, fontweight="bold")

    def de(x1, y1, x2, y2, label, r=0.35):
        ax.annotate("", xy=(x2, y2+r), xytext=(x1, y1-r),
                     arrowprops=dict(arrowstyle="-", color="#555", lw=1.2))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx-0.3, my+0.1, label, fontsize=10, color="#c62828", fontweight="bold")

    for n in l1: dn(*n)
    for n in l2: dn(*n)

    de(root[0], root[1], l1[0][0], l1[0][1], "3/8")
    de(root[0], root[1], l1[1][0], l1[1][1], "5/8")

    de(l1[0][0], l1[0][1], l2[0][0], l2[0][1], "2/7")
    de(l1[0][0], l1[0][1], l2[1][0], l2[1][1], "5/7")
    de(l1[1][0], l1[1][1], l2[2][0], l2[2][1], "3/7")
    de(l1[1][0], l1[1][1], l2[3][0], l2[3][1], "4/7")

    ax.text(-0.4, 3.6, "1. Zug", fontsize=11, fontstyle="italic", color="#555")
    ax.text(-0.4, 1.5, "2. Zug", fontsize=11, fontstyle="italic", color="#555")

    ax.text(0.5, -0.2, "g = gebraucht, n = neu    (ohne Zurücklegen!)", fontsize=9, color="#555")

    fig.tight_layout()
    return fig_to_b64(fig)

# ═══════════════════════════════════════════════════════════════════
# Generate all images
# ═══════════════════════════════════════════════════════════════════
print("Generating images...")
img_coin_tree = make_coin_tree()
img_coin_table = make_coin_table()
img_spinner_tree = make_spinner_tree()
img_addition_tree = make_addition_tree()
img_empty_tree = make_empty_tree()
img_basketball_tree = make_basketball_tree()
img_tennis_tree = make_tennis_tree()
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

def header_box(title):
    """Standard header with title left + Dr. Winkelmann right."""
    return f'''<stroke tool="pen" color="#000000ff" width="0.77205084" capStyle="round">14.17 28.34 14.17 14.17 481.78 14.17 481.78 28.34 14.17 28.34</stroke>
<text font="Sans" size="12" x="17.20" y="14.60" color="#000000ff">{title}</text>
<text font="Sans" size="12" x="496.97" y="15.34" color="#000000ff">Dr. Winkelmann</text>
<stroke tool="pen" color="#000000ff" width="0.85" capStyle="round">495.95 14.17 495.95 28.34 580.97 28.34 580.97 14.17 495.95 14.17</stroke>'''

def phase_box(label, y_top=42.51):
    """Phase label in a box spanning full width."""
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
p1 = page_start()
p1 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p1 += text_block(16.37, 42.60, """Vorbereitung für Lehrkraft – NICHT für Schüler sichtbar

Lernziele / Kompetenzen:
- Die SuS können mehrstufige Zufallsexperimente in
  Baumdiagrammen darstellen.
- Die SuS kennen und anwenden die Pfadmultiplikationsregel.
- Die SuS kennen und anwenden die Pfadadditionsregel.
- Die SuS unterscheiden abhängige und unabhängige Stufen.

Einordnung in die Sequenz:
- Vorwissen: 6.1 Baumdiagramme (Grundlagen, Ergebnismengen)
- Diese Stunde: Berechnung von Wahrscheinlichkeiten mit
  Pfadregeln
- Ausblick: Anwendung auf komplexere Zufallsexperimente

Verlaufsplan (90 Minuten):
┌──────────┬──────────────────────────────────┬───────┬────────┐
│ Phase    │ Inhalt                           │ Zeit  │ Form   │
├──────────┼──────────────────────────────────┼───────┼────────┤
│ Einstieg │ Einstiegsproblem: Münzwurf       │ 10min │ Plenum │
│ Erarb. I │ Pfadmultiplikationsregel         │ 15min │ PA     │
│ Sicherung│ Merksatz Pfadmultiplikation      │  5min │ Plenum │
│ Erarb.II │ Pfadadditionsregel               │ 12min │ PA     │
│ Sicherung│ Merksatz Pfadaddition            │  5min │ Plenum │
│ Übung I  │ Basisaufgaben S.181, Nr.1-3      │ 18min │ EA     │
│ Vertiefg.│ Abhängige Stufen (Bsp.3, S.183) │ 10min │ Plenum │
│ Übung II │ Weiterf. Aufgaben S.183, Nr.8    │ 10min │ PA     │
│ HA       │ Hausaufgabe festlegen            │  5min │ Plenum │
└──────────┴──────────────────────────────────┴───────┴────────┘

Material: Schulbuch S. 180–185, Beamer/Tablet

Didaktische Hinweise:
- Kernidee: Wahrscheinlichkeiten entlang der Pfade
  multiplizieren, für Ereignisse addieren.
- Typische Fehler: Addition statt Multiplikation entlang
  eines Pfades; Vergessen der Pfadaddition bei Ereignissen
  mit mehreren Pfaden.
- Differenzierung: Basisaufgaben für alle, Nr. 11-12 als
  Zusatz für Schnelle.

Diagnosefragen:
- „Wie berechnest du die Wahrscheinlichkeit für einen
   bestimmten Pfad?"
- „Wann musst du Wahrscheinlichkeiten addieren?"

Reserve: Aufgabe 4 (S.181) – Glücksräder""", size="10")
p1 += page_end()
pages.append(p1)

# ─── PAGE 2: Einstieg ─────────────────────────────────────────────
p2 = page_start()
p2 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p2 += phase_box("Einstieg:")
p2 += text_block(16.37, 62.0, """Eine Münze wird zweimal geworfen.

Leitfrage: Wie groß ist die Wahrscheinlichkeit,
zweimal „Kopf" zu werfen?

1) Zeichne ein Baumdiagramm für den zweifachen Münzwurf.
2) Welche Ergebnisse sind möglich? Notiere alle.
3) Überlege: Wie könnte man die Wahrscheinlichkeit
   für ein bestimmtes Ergebnis berechnen?""", size="12")
p2 += image_tag(60, 250, 470, 500, img_coin_tree)
p2 += text_block(16.37, 520, "(EA, ca. 5 Minuten – dann Besprechung im Plenum)", size="10", color="#999999ff")
p2 += page_end()
pages.append(p2)

# ─── PAGE 3: Erarbeitung I – Pfadmultiplikationsregel ─────────────
p3 = page_start()
p3 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p3 += phase_box("Erarbeitung I: Pfadmultiplikationsregel")
p3 += text_block(16.37, 62.0, """Beispiel 1: Ein Glücksrad mit den Farben Rot (⅔) und
Blau (⅓) wird zweimal gedreht.
Wie groß ist die Wahrscheinlichkeit, zweimal Rot
zu erhalten?""", size="12")
p3 += image_tag(40, 145, 520, 420, img_spinner_tree)
p3 += text_block(16.37, 435, """Beobachtung:
Die Wahrscheinlichkeit für (Rot; Rot) erhält man,
indem man die Einzelwahrscheinlichkeiten entlang
des Pfades multipliziert:

P(Rot; Rot) = ⅔ · ⅔ = 4/9""", size="12")
p3 += image_tag(40, 600, 470, 740, img_coin_table)
p3 += text_block(16.37, 755, """Prüfe: Die Summe aller Ergebnis-Wahrscheinlichkeiten
muss 1 (= 100 %) ergeben.""", size="11", color="#555555ff")
p3 += page_end()
pages.append(p3)

# ─── PAGE 4: Sicherung I – Merksatz Pfadmultiplikation ────────────
p4 = page_start()
p4 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p4 += phase_box("Sicherung I: Pfadmultiplikationsregel")
p4 += text_block(16.37, 70.0, """MERKSATZ – Pfadmultiplikationsregel:

Die Wahrscheinlichkeit für ein zusammengesetztes
Ergebnis erhält man, indem man die
Einzelwahrscheinlichkeiten längs des zugehörigen
Pfades multipliziert.""", size="12")
p4 += text_block(16.37, 195.0, """Für mehrstufige Zufallsexperimente gilt außerdem:
• Die Wahrscheinlichkeiten der zusammengesetzten
  Ergebnisse am Ende der Pfade addieren sich zu 1
  (100 %).
• Die Summe der Wahrscheinlichkeiten unter jeder
  Verzweigung ist 1 (100 %).""", size="11")

# Platz für Schülernotizen
p4 += text_block(16.37, 340, "(Platz für eigene Notizen und Beispiele)", size="10", color="#999999ff")
p4 += page_end()
pages.append(p4)

# ─── PAGE 5: Erarbeitung II – Pfadadditionsregel ──────────────────
p5 = page_start()
p5 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p5 += phase_box("Erarbeitung II: Pfadadditionsregel")
p5 += text_block(16.37, 62.0, """Münze wird zweimal geworfen. Wie groß ist die
Wahrscheinlichkeit für das Ereignis
„einmal Kopf und einmal Zahl"?

Dieses Ereignis besteht aus zwei Pfaden:
  (Kopf; Zahl)  und  (Zahl; Kopf)""", size="12")
p5 += image_tag(30, 185, 530, 485, img_addition_tree)
p5 += text_block(16.37, 500, """Beobachtung: Wenn ein Ereignis aus mehreren Pfaden
besteht, addiert man die Einzelwahrscheinlichkeiten
der zugehörigen Pfade.""", size="12")
p5 += page_end()
pages.append(p5)

# ─── PAGE 6: Sicherung II – Merksatz Pfadaddition ─────────────────
p6 = page_start()
p6 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p6 += phase_box("Sicherung II: Pfadadditionsregel")
p6 += text_block(16.37, 70.0, """MERKSATZ – Pfadadditionsregel:

Die Wahrscheinlichkeit für ein Ereignis erhält man,
indem man die Wahrscheinlichkeiten der zugehörigen
Pfade addiert.""", size="12")
p6 += text_block(16.37, 175.0, """Beispiel:
P(„einmal Kopf, einmal Zahl")
  = P(Kopf; Zahl) + P(Zahl; Kopf)
  = ½ · ½  +  ½ · ½
  = ¼ + ¼ = ½""", size="12")
p6 += text_block(16.37, 320, "(Platz für eigene Notizen und Beispiele)", size="10", color="#999999ff")
p6 += page_end()
pages.append(p6)

# ─── PAGE 7: Übung I – Basisaufgaben ──────────────────────────────
p7 = page_start()
p7 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p7 += phase_box("Übung I – Basisaufgaben (EA, S.181):")
p7 += text_block(16.37, 62.0, """Aufgabe 1 (S. 181):
Karla zieht zweimal hintereinander eine Kugel und
legt sie wieder zurück. Als Ergebnis notiert sie
(Gelb; Gelb).
a) Was bedeutet das zusammengesetzte Ergebnis
   (Gelb; Gelb)? Beschreibe mit eigenen Worten.
b) Erstelle ein Baumdiagramm und beschreibe alle
   zusammengesetzten Ergebnisse, bei denen zuerst
   eine blaue Kugel gezogen wird.

Zeichne dein Baumdiagramm hier:""", size="11")
p7 += image_tag(60, 290, 470, 530, img_empty_tree)
p7 += text_block(16.37, 545, """Aufgabe 2 (S. 181):
Das Glücksrad wird zweimal gedreht.
a) Zeichne das zugehörige Baumdiagramm und trage die
   Wahrscheinlichkeiten an den Zweigen ein.
b) Welche zusammengesetzten Ergebnisse sind möglich?
   Bestimme jeweils die Wahrscheinlichkeit.
c) Kontrolliere deine Rechnung, indem du prüfst, ob
   die Summe aller Wahrscheinlichkeiten 1 ergibt.""", size="11")
p7 += page_end()
pages.append(p7)

# ─── PAGE 8: Übung I – Fortsetzung ───────────────────────────────
p8 = page_start()
p8 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p8 += phase_box("Übung I – Fortsetzung (EA, S.181):")
p8 += text_block(16.37, 62.0, """Aufgabe 3 (S. 181):
Jannes trifft den Korb beim Basketball-Freiwurf mit
einer Wahrscheinlichkeit von 0,6 und verfehlt ihn
mit einer Wahrscheinlichkeit von 0,4. Er wirft
dreimal.
a) Zeichne ein Baumdiagramm mit Wahrscheinlichkeiten.
b) Berechne die Wahrscheinlichkeit dafür, dass
   Jannes dreimal trifft.
c) Berechne die Wahrscheinlichkeit für das Ergebnis
   (Korb; Korb; kein Korb).""", size="11")
p8 += text_block(16.37, 240, "Vorlage für dein Baumdiagramm:", size="10", color="#999999ff")
p8 += image_tag(20, 265, 560, 600, img_basketball_tree)
p8 += text_block(16.37, 610, """Platz für Berechnungen:

b) P(T; T; T) =



c) P(T; T; K) =""", size="11")
p8 += page_end()
pages.append(p8)

# ─── PAGE 9: Vertiefung – Abhängige Stufen ────────────────────────
p9 = page_start()
p9 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p9 += phase_box("Vertiefung: Baumdiagramme mit abhängigen Stufen")
p9 += text_block(16.37, 62.0, """Beispiel 3 (S. 183): Aus einer Kiste mit 5 neuen und
3 gebrauchten Tennisbällen werden zwei Bälle
entnommen (ohne Zurücklegen!).
Wie groß ist die Wahrscheinlichkeit, dass es ein
gebrauchter und ein neuer Ball sind?

Wichtig: Beim 2. Zug ändert sich die Gesamtzahl!""", size="12")
p9 += image_tag(30, 215, 520, 465, img_tennis_tree)
p9 += text_block(16.37, 485, """E: einmal gebraucht, einmal neu
P(E) = P(g; n) + P(n; g)
     = 3/8 · 5/7  +  5/8 · 3/7
     = 15/56 + 15/56 = 30/56 ≈ 54 %""", size="12")
p9 += text_block(16.37, 610, """Merke: Wenn die Objekte NICHT zurückgelegt werden,
ändern sich die Wahrscheinlichkeiten in der
nächsten Stufe → „abhängige Stufen".""", size="11", color="#555555ff")
p9 += page_end()
pages.append(p9)

# ─── PAGE 10: Übung II – Weiterführend ────────────────────────────
p10 = page_start()
p10 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p10 += phase_box("Übung II – Weiterführend (PA, S.183):")
p10 += text_block(16.37, 62.0, """Aufgabe 8 (S. 183):
In einem Gefäß liegen drei weiße und zwei schwarze
Kugeln. Zwei Kugeln werden nacheinander zufällig
entnommen.
a) Zeichne ein Baumdiagramm und berechne die
   Wahrscheinlichkeit, dass zwei gleiche Kugeln
   gezogen werden, wenn gezogene Kugeln
   zurückgelegt (nicht zurückgelegt) werden.
b) Erkläre anschaulich, warum die Wahrscheinlichkeit
   in dem einen Fall größer ist.

Zeichne dein Baumdiagramm hier:""", size="11")
p10 += image_tag(60, 310, 470, 550, img_empty_tree)
p10 += text_block(16.37, 570, """Berechnung:

a) Mit Zurücklegen:
   P(gleiche Farbe) =


   Ohne Zurücklegen:
   P(gleiche Farbe) =


b) Begründung:""", size="11")
p10 += page_end()
pages.append(p10)

# ─── PAGE 11: Hausaufgabe ─────────────────────────────────────────
p11 = page_start()
p11 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p11 += phase_box("Hausaufgabe:")
p11 += text_block(16.37, 62.0, """Pflicht:
  Buch S. 181, Aufgabe 4
  (Zwei Glücksräder werden gleichzeitig gedreht.)

Zusatz für Schnelle:
  Buch S. 184, Aufgabe 11
  (Drei Karten mit Ziffern 2, 3 und 7.)""", size="12")
p11 += text_block(16.37, 220, """Aufgabe 4 (S. 181):
Die beiden Glücksräder werden gleichzeitig gedreht.
a) Zeichne ein Baumdiagramm mit der Farbe des
   linken Glücksrads als 1. Stufe und mit der Farbe
   des rechten Glücksrads als 2. Stufe. Trage die
   Wahrscheinlichkeiten ein.
b) Zeichne ein Baumdiagramm mit der Farbe des
   rechten Glücksrads als 1. Stufe und mit der Farbe
   des linken Glücksrads als 2. Stufe. Trage die
   Wahrscheinlichkeiten ein.
c) Bestimme die Wahrscheinlichkeit, dass beide
   Glücksräder Rot zeigen. Verwende einmal das
   Baumdiagramm in a) und einmal das in b).
   Vergleiche die Ergebnisse.""", size="11")
p11 += page_end()
pages.append(p11)

# ─── PAGE 12: Lösungen ────────────────────────────────────────────
p12 = page_start()
p12 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p12 += phase_box("Lösungen und Hinweise – Nur für die Lehrkraft:")
p12 += text_block(16.37, 65.0, """Einstieg – Münzwurf:
P(K;K) = ½ · ½ = ¼ = 25 %
Alle Ergebnisse: (K;K), (K;Z), (Z;K), (Z;Z),
je 25 %.

Beispiel 1 – Glücksrad:
P(Rot; Rot) = ⅔ · ⅔ = 4/9 ≈ 44,4 %

Aufgabe 1:
a) (Gelb; Gelb) bedeutet: beim 1. und 2. Ziehen
   wurde jeweils eine gelbe Kugel gezogen.
b) Zusammengesetzte Ergebnisse mit Blau zuerst:
   (Blau; Gelb), (Blau; Blau), (Blau; Rot) usw.

Aufgabe 2:
Abhängig von der Farbverteilung des Glücksrads.
Summe aller Wahrscheinlichkeiten muss 1 ergeben.

Aufgabe 3:
b) P(T;T;T) = 0,6 · 0,6 · 0,6 = 0,216 = 21,6 %
c) P(T;T;K) = 0,6 · 0,6 · 0,4 = 0,144 = 14,4 %

Aufgabe 8:
a) Mit Zurücklegen:
   P(ww) = 3/5 · 3/5 = 9/25
   P(ss) = 2/5 · 2/5 = 4/25
   P(gleich) = 9/25 + 4/25 = 13/25 = 52 %

   Ohne Zurücklegen:
   P(ww) = 3/5 · 2/4 = 6/20
   P(ss) = 2/5 · 1/4 = 2/20
   P(gleich) = 6/20 + 2/20 = 8/20 = 40 %

b) Ohne Zurücklegen ist P(gleich) kleiner, weil
   nach Ziehen einer Farbe weniger Kugeln dieser
   Farbe übrig sind.""", size="10")
p12 += page_end()
pages.append(p12)

# ─── PAGE 13: Lösungen Fortsetzung ────────────────────────────────
p13 = page_start()
p13 += header_box("Mathe - Mehrstufige Zufallsexperimente: 6.2 Wahrscheinlichkeiten bei Baumdiagrammen")
p13 += phase_box("Lösungen – Fortsetzung:")
p13 += text_block(16.37, 65.0, """Beispiel 3 (Tennisbälle, abhängige Stufen):
P(E) = P(g;n) + P(n;g)
     = 3/8 · 5/7 + 5/8 · 3/7
     = 15/56 + 15/56 = 30/56 ≈ 53,6 %

Pfadadditionsregel – Beispiel:
P(„einmal Kopf, einmal Zahl")
  = P(K;Z) + P(Z;K) = ¼ + ¼ = ½ = 50 %

Typische Schülerfehler:
- Addition statt Multiplikation entlang eines Pfades
- Vergessen, dass bei „ohne Zurücklegen" sich die
  Wahrscheinlichkeiten ändern
- Pfade für ein Ereignis vergessen (nur einen Pfad
  statt alle zugehörigen berechnen)

Impulse / Fragetechniken:
- „Was passiert mit der Gesamtzahl, wenn du eine
   Kugel nicht zurücklegst?"
- „Wie viele Pfade gehören zu deinem Ereignis?"
- „Prüfe: Ergeben alle Pfad-Wahrscheinlichkeiten
   zusammen genau 1?"

Hausaufgabe 4 (S. 181):
c) P(Rot; Rot) ist in beiden Baumdiagrammen gleich.
   Die Reihenfolge der Stufen ändert nichts an der
   Ergebnis-Wahrscheinlichkeit.""", size="10")
p13 += page_end()
pages.append(p13)

# ═══════════════════════════════════════════════════════════════════
# ASSEMBLE XML AND WRITE GZIPPED .xopp
# ═══════════════════════════════════════════════════════════════════
xml = '<?xml version="1.0" standalone="no"?>\n'
xml += '<xournal creator="xournalpp 1.2.7" fileversion="4">\n'
xml += '<title>Xournal++ document - see https://xournalpp.github.io/</title>\n'
for p in pages:
    xml += p + "\n"
xml += "</xournal>\n"

out_path = os.path.join(OUT_DIR, "6.2 Wahrscheinlichkeiten bei Baumdiagrammen.xopp")
with gzip.open(out_path, "wb") as f:
    f.write(xml.encode("utf-8"))

print(f"Done! File saved to: {out_path}")
print(f"XML size: {len(xml)} bytes")
print(f"Pages: {len(pages)}")
