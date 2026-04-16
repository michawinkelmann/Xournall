#!/usr/bin/env python3
"""
preview_crops.py — Extrahiert alle Bildausschnitte aus einem plan.json und speichert sie als einzelne PNGs.

Zweck: Claude kann die Ausschnitte visuell inspizieren (mit dem view-Tool) und die
Crop-Koordinaten korrigieren, BEVOR die .xopp-Datei generiert wird.

Verwendung:
    python3 preview_crops.py plan.json [output_dir]

Ausgabe:
    - Einzelne PNG-Dateien pro Crop im output_dir (Standard: ./crop_previews/)
    - Konsolenausgabe mit Dateinamen, Quellbild, Crop-Koordinaten und Pixelgrößen
"""

import json
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("FEHLER: Pillow nicht installiert. Bitte 'pip install Pillow' ausführen.")
    sys.exit(1)


def extract_crop(img_path, crop, output_path):
    """Schneidet einen Bereich aus einem Bild und speichert ihn."""
    if not os.path.exists(img_path):
        print(f"  FEHLER: Datei nicht gefunden: {img_path}")
        return None

    img = Image.open(img_path)
    w, h = img.size

    if "left_px" in crop:
        left   = int(crop.get("left_px", 0))
        top    = int(crop.get("top_px", 0))
        right  = int(crop.get("right_px", w))
        bottom = int(crop.get("bottom_px", h))
        mode = "pixel"
    else:
        left   = int(w * crop.get("left", 0) / 100)
        top    = int(h * crop.get("top", 0) / 100)
        right  = int(w * crop.get("right", 100) / 100)
        bottom = int(h * crop.get("bottom", 100) / 100)
        mode = "prozent"

    # Clamp
    left   = max(0, min(left, w - 1))
    top    = max(0, min(top, h - 1))
    right  = max(left + 1, min(right, w))
    bottom = max(top + 1, min(bottom, h))

    cropped = img.crop((left, top, right, bottom))
    cropped.save(output_path, format='PNG')

    return {
        "source_size": f"{w}x{h}",
        "crop_mode": mode,
        "crop_box": f"({left}, {top}, {right}, {bottom})",
        "result_size": f"{cropped.size[0]}x{cropped.size[1]}",
        "output": output_path
    }


def preview_all_crops(plan_path, output_dir="./crop_previews"):
    """Extrahiert alle Bild-Crops aus plan.json und speichert sie als PNGs."""
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    crop_index = 0
    results = []

    # Durchsuche alle Phasen nach Bild-Elementen
    for phase in plan.get("phasen", []):
        phase_name = phase.get("name", "unbekannt")
        for item in phase.get("inhalte", []):
            if item.get("type") == "bild" and item.get("crop"):
                crop_index += 1
                safe_name = phase_name.replace(" ", "_").replace("/", "-")
                filename = f"crop_{crop_index:02d}_{safe_name}.png"
                output_path = os.path.join(output_dir, filename)

                print(f"\n--- Crop {crop_index}: Phase '{phase_name}' ---")
                print(f"  Quelle: {item['path']}")
                print(f"  Crop:   {item['crop']}")

                info = extract_crop(item["path"], item["crop"], output_path)
                if info:
                    print(f"  Quellbild:  {info['source_size']} px")
                    print(f"  Modus:      {info['crop_mode']}")
                    print(f"  Box:        {info['crop_box']}")
                    print(f"  Ergebnis:   {info['result_size']} px")
                    print(f"  Gespeichert: {output_path}")
                    results.append({
                        "index": crop_index,
                        "phase": phase_name,
                        "file": output_path,
                        **info
                    })

    # Auch Lösungen durchsuchen
    for item in plan.get("loesungen", []):
        if item.get("type") == "bild" and item.get("crop"):
            crop_index += 1
            filename = f"crop_{crop_index:02d}_loesungen.png"
            output_path = os.path.join(output_dir, filename)
            print(f"\n--- Crop {crop_index}: Lösungen ---")
            print(f"  Quelle: {item['path']}")
            print(f"  Crop:   {item['crop']}")
            info = extract_crop(item["path"], item["crop"], output_path)
            if info:
                print(f"  Ergebnis: {info['result_size']} px")
                print(f"  Gespeichert: {output_path}")
                results.append({
                    "index": crop_index,
                    "phase": "Lösungen",
                    "file": output_path,
                    **info
                })

    print(f"\n{'='*50}")
    print(f"Fertig: {len(results)} Crops extrahiert nach {output_dir}/")
    print(f"Bitte jeden Crop einzeln mit dem view-Tool prüfen!")
    print(f"{'='*50}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python3 preview_crops.py plan.json [output_dir]")
        sys.exit(1)

    plan_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./crop_previews"
    preview_all_crops(plan_path, output_dir)
