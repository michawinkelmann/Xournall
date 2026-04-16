# JSON-Schema: Minimaler Unterrichtsplan für .xopp-Generierung

Das Skript `scripts/generate_xopp.py` erwartet eine JSON-Datei. Für den Minimal-Skill nutzen wir es mit vier Phasen, ohne Vorbereitungsseite und ohne Lösungen in der .xopp. Lösungen kommen in eine separate PDF.

## Grundstruktur

```json
{
  "fach": "Mathematik",
  "jahrgangsstufe": "Klasse 10",
  "sequenzthema": "Periodische Vorgänge",
  "stundenthema": "Sinusfunktion und Kosinusfunktion",
  "annahmen": "",
  "skip_vorbereitung": true,
  "phasen": [
    {
      "name": "Einstieg",
      "inhalte": [ ... ]
    },
    {
      "name": "Erarbeitung",
      "inhalte": [ ... ]
    },
    {
      "name": "Übungsaufgaben",
      "inhalte": [ ... ]
    },
    {
      "name": "Vertiefungsaufgaben",
      "inhalte": [ ... ]
    }
  ],
  "loesungen": {
    "Einstieg (Denkanstoß)": [ ... ],
    "Erarbeitung": [ ... ],
    "Übungsaufgaben": [ ... ],
    "Vertiefungsaufgaben": [ ... ]
  }
}
```

**Wichtig:**
- `"skip_vorbereitung": true` — Keine leere Lehrerseite generieren.
- Kein `"vorbereitung"`-Feld nötig.
- `"loesungen"` ist ein Dict, gegliedert nach Phasen — wird von `generate_loesungen_pdf.py` verarbeitet.

## Verfügbare Inhalts-Typen

### text
```json
{ "type": "text", "content": "Der Text...", "color": "#000000ff", "size": 12 }
```
- `color`: optional. Blau: `"#3333ccff"`, Rot: `"#cc0000ff"`, Grau: `"#808080ff"`
- `size`: optional, Standard 12

### aufgabe
```json
{ "type": "aufgabe", "nr": "1", "content": "Beschreibe den Sachverhalt." }
```

### merksatz
```json
{ "type": "merksatz", "content": "Die Sinusfunktion hat die Gleichung f(α) = sin(α)." }
```

### freiraum
```json
{ "type": "freiraum", "hoehe": 150, "label": "Platz für deine Rechnung:" }
```

### koordinatensystem
```json
{
  "type": "koordinatensystem",
  "x": 50, "width": 250, "height": 200,
  "x_label": "α", "y_label": "y",
  "x_min": 0, "x_max": 360, "y_min": -1, "y_max": 1
}
```

### tabelle
```json
{
  "type": "tabelle",
  "rows": 6, "cols": 3,
  "col_width": 100, "row_height": 22,
  "headers": ["α", "sin(α)", "cos(α)"]
}
```

### bild
```json
{
  "type": "bild",
  "path": "/path/to/buchseite.png",
  "crop": {"left_px": 100, "top_px": 50, "right_px": 800, "bottom_px": 270},
  "buchseite": "S. 181"
}
```
- Pixel-Koordinaten haben Vorrang vor Prozentwerten.
- **`buchseite` ist Pflicht** bei Buchausschnitten. Wird als kleine graue Referenz über dem Bild angezeigt.

### linie
```json
{ "type": "linie" }
```

## Phasen-Namen (Minimal-Skill)
- `Einstieg` → Denkanstoß (bekommt den zweizeiligen Header)
- `Erarbeitung` → Gemeinsames Erarbeiten
- `Übungsaufgaben` → Basisaufgaben
- `Vertiefungsaufgaben` → Weiterführende Aufgaben

## Lösungs-Typen (für die PDF)

Im `"loesungen"`-Dict können folgende Typen verwendet werden:

### text
```json
{ "type": "text", "content": "Erklärungstext oder Ergebnis." }
```

### aufgabe
```json
{ "type": "aufgabe", "nr": "1", "loesung": "a) 1,57  b) 0,79  c) 0,17  d) 3,14" }
```
Oder mit mehreren Zeilen:
```json
{ "type": "aufgabe", "nr": "7a", "loesung": ["0° → 0", "90° → π/2 ≈ 1,57", "240° → 4π/3 ≈ 4,19"] }
```

### tabelle
```json
{
  "type": "tabelle",
  "headers": ["Gradmaß", "Bogenmaß"],
  "rows": [["0°", "0"], ["90°", "π/2 ≈ 1,57"], ["180°", "π ≈ 3,14"]]
}
```

### ueberschrift
```json
{ "type": "ueberschrift", "content": "Zu den Beispielrechnungen" }
```

### linie
```json
{ "type": "linie" }
```

## Tipps
- **Freiraum großzügig**: Mind. ein `freiraum`-Block pro Seite.
- **Nur Aufgaben als Bild**: Merksätze immer selbst schreiben.
- **Ausschnitte passgenau**: Pro Aufgabe ein eigener Crop.
- **Buchseite immer angeben**: Jeder Crop braucht `"buchseite": "S. XXX"`.
- **Echte Umlaute**: JSON mit `json.dump(..., ensure_ascii=False)` schreiben.
- **Keine Denkanstoß-Überschrift**: Einstieg beginnt direkt mit dem Impuls.
- **Lösungen vollständig**: Zu jeder Aufgabe und jedem Beispiel die Lösung angeben.
