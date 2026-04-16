# JSON-Schema: Unterrichtsplan für .xopp-Generierung

Das Skript `scripts/generate_xopp.py` erwartet eine JSON-Datei mit folgendem Aufbau:

## Grundstruktur

```json
{
  "fach": "Mathematik",
  "jahrgangsstufe": "Klasse 8",
  "sequenzthema": "Lineare Gleichungssysteme",
  "stundenthema": "Lineare Gleichungen mit zwei Variablen",
  "annahmen": "Schüler kennen lineare Gleichungen mit einer Variablen, Funktionsbegriff eingeführt.",

  "vorbereitung": "Mehrzeiliger Text mit:\n- Lernzielen\n- Verlaufsplan\n- Didaktischen Hinweisen\n- Material\n- Reserve-Optionen",

  "phasen": [
    {
      "name": "Einstieg",
      "inhalte": [ ... ]
    },
    {
      "name": "Erarbeitung I",
      "inhalte": [ ... ]
    },
    ...
  ],

  "loesungen": [
    { "type": "text", "content": "Lösungen zu allen Aufgaben..." }
  ]
}
```

## Verfügbare Inhalts-Typen in `inhalte`

### text
Normaler Text, z.B. Erklärungen, Überschriften.
```json
{ "type": "text", "content": "Der Text...", "color": "#000000ff", "size": 12 }
```
- `color`: optional, Standard schwarz. Blau: `"#3333ccff"`, Rot: `"#cc0000ff"`, Grau: `"#808080ff"`
- `size`: optional, Standard 12

### aufgabe
Nummerierter Arbeitsauftrag (wird blau dargestellt).
```json
{ "type": "aufgabe", "nr": "1", "content": "Beschreibe den Sachverhalt mit einer linearen Gleichung." }
```

### merksatz
Hervorgehobener Merksatz in blauer Box.
```json
{ "type": "merksatz", "content": "Eine Gleichung der Form a·x + b·y = c heißt lineare Gleichung mit zwei Variablen." }
```

### freiraum
Leerer Platz zum Rechnen, Skizzieren, Ergänzen.
```json
{ "type": "freiraum", "hoehe": 150, "label": "Platz für deine Rechnung:" }
```
- `hoehe`: Pixel, Standard 150. Großzügig bemessen!
- `label`: optional, wird klein/grau über dem Freiraum angezeigt

### koordinatensystem
Leeres Koordinatensystem mit Achsen und Skalenstrichen.
```json
{
  "type": "koordinatensystem",
  "x": 50, "width": 250, "height": 200,
  "x_label": "x", "y_label": "y",
  "x_min": -2, "x_max": 8, "y_min": -1, "y_max": 7
}
```

### tabelle
Leere Tabelle mit optionalen Kopfzeilen.
```json
{
  "type": "tabelle",
  "rows": 6, "cols": 3,
  "col_width": 100, "row_height": 22,
  "headers": ["x", "y", "Prüfung"]
}
```

### bild
Eingebetteter Bildausschnitt aus dem Buch. **Nur für Aufgaben verwenden** — nicht für Merksätze, Definitionen oder Erklärungstexte (die schreibst du selbst als text/merksatz-Elemente).

```json
{
  "type": "bild",
  "path": "/path/to/buchseite.png",
  "crop": {"left": 51.5, "top": 4.0, "right": 78.0, "bottom": 12.5}
}
```

**Crop-Angabe (Pflicht bei Buchseiten!):**

Variante A — Prozentwerte (Dezimalstellen erlaubt):
```json
"crop": {"left": 51.5, "top": 4.0, "right": 78.0, "bottom": 12.5}
```

Variante B — Pixel-Koordinaten (genauer, wenn Bildgröße bekannt):
```json
"crop": {"left_px": 988, "top_px": 50, "right_px": 1500, "bottom_px": 155}
```
Pixel-Koordinaten haben Vorrang wenn beide angegeben.

- `width`: optional, Anzeigebreite in xopp-Punkten. Ohne Angabe wird automatisch skaliert.
- Das Skript skaliert proportional und begrenzt auf die Seitenbreite. Kein Element ragt über den Rand.
- Automatischer Seitenumbruch wenn das Bild nicht mehr auf die aktuelle Seite passt.

**Regeln für Ausschnitte:**
- **Passgenau**: Nur die eine Aufgabe, nichts von Nachbar-Aufgaben
- **Vollständig**: Aufgabennummer, alle Teilaufgaben, Hinweise, zugehörige Skizzen
- **Kleiner Puffer**: ~0.5% oder ~5px Rand als Sicherheit, aber nicht mehr
- **Kein Abschnitt**: Kein abgeschnittener Text am Rand des Ausschnitts

### linie
Horizontale Trennlinie.
```json
{ "type": "linie" }
```

## Phasen-Namen

Übliche Phasennamen (passend zum Template):
- `Einstieg` (bekommt die spezielle Doppel-Header-Darstellung wie Seite 2)
- `Erarbeitung I`
- `Sicherung`
- `Erarbeitung II`
- `Übungen I - Basis`
- `Übungen II - Weiterführend`
- `Hausaufgabe`
- `Reserve`

Andere Namen sind möglich, verwenden dann den einfachen Header-Stil.

## Tipps

- **Freiraum großzügig**: Jede Schülerseite sollte mindestens einen `freiraum`-Block haben. Das Skript kürzt Freiräume automatisch wenn nötig.
- **Nur Aufgaben als Bild**: Merksätze, Definitionen, Erklärungen immer selbst schreiben — nie als Bild einfügen.
- **Ausschnitte passgenau**: Pro Aufgabe ein eigener Crop. Nichts von Nachbar-Aufgaben sichtbar.
- **Merksatz fertig formulieren**: In der Sicherung muss der Merksatz komplett stehen (als `merksatz`-Element).
- **Aufgaben imperativisch**: "Berechne...", "Beschreibe...", "Zeichne..."
- **Automatischer Seitenumbruch**: Das Skript erstellt Fortsetzungsseiten wenn eine Phase nicht auf eine Seite passt.
- **Echte Umlaute verwenden**: Alle Textinhalte müssen ä, ö, ü, ß enthalten — niemals ae, oe, ue, ss als Ersatz. JSON mit `json.dump(..., ensure_ascii=False)` schreiben.
