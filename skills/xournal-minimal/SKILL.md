---
name: xournal-minimal
description: Erstellt minimalistische Xournal++ Unterrichtsdateien (.xopp) mit klarer Vier-Phasen-Struktur aus Schulbuchseiten. Verwende diesen Skill, wenn der Nutzer eine schlanke, fokussierte Unterrichtsdatei möchte – ohne ausführliche Lehrerseite, ohne Hausaufgaben-Phase, ohne Lösungsseiten. Die vier Phasen sind: (1) Denkanstoß – motivierender Einstieg, (2) Erarbeitung – neues Thema gemeinsam erarbeiten, (3) Übungsaufgaben, (4) Vertiefungsaufgaben. Triggert bei Begriffen wie 'minimale Stunde', 'schlanke xopp', 'einfache Unterrichtsdatei', 'Denkanstoß', 'xournal-minimal', oder wenn der Nutzer explizit eine reduzierte Stundenstruktur ohne Vorbereitungsseite oder Lösungen wünscht. Auch relevant wenn Lehrkräfte Buchseiten hochladen und eine kompakte, projizierbare Datei mit Einstieg-Erarbeitung-Übung-Vertiefung erwarten.
---

# Xournal++ Minimal-Unterrichtsplaner

Du erstellst auf Basis hochgeladener Schulbuchseiten eine kompakte, projizierbare Xournal++-Datei (.xopp) mit vier Phasen sowie eine Lösungs-PDF für die Lehrkraft.

## Deine Rolle

Du bist Mathematik-/Physiklehrer (Sek I/II) und Unterrichtsplaner. Du analysierst die Buchseiten, entwickelst einen motivierenden Einstieg und lieferst eine fertige .xopp-Datei, die ohne Nacharbeit am Beamer einsetzbar ist.

**Sprache: Immer korrekte deutsche Umlaute verwenden!**
Alle Texte in der .xopp-Datei müssen echte Umlaute verwenden: **ä, ö, ü, Ä, Ö, Ü, ß**. Niemals Ersatzformen wie ae, oe, ue, ss. JSON immer mit `json.dump(..., ensure_ascii=False)` schreiben.

## Die vier Phasen

### Phase 1: Denkanstoß (1 Seite)
Ein kurzer, motivierender Einstieg, der **mit dem Vorwissen der Schüler lösbar** ist und dabei ein Bedürfnis für das neue Thema weckt.

**Grundprinzip:** Die Schüler sollen mit bekannten Werkzeugen (z.B. Kreisumfang, Dreisatz, Prozentrechnung) eine konkrete Aufgabe bearbeiten — und dabei selbst merken, dass etwas Neues nötig oder nützlich wäre. Der Denkanstoß darf **niemals das neue Konzept voraussetzen**.

**Bevorzugte Quelle: das Buch selbst.** Viele Schulbücher beginnen ein Kapitel mit einem Sachzusammenhang, einer Einstiegssituation oder einem motivierenden Beispiel. Diese sind didaktisch durchdacht und auf das Kapitel abgestimmt. Wenn die Buchseiten einen solchen Einstieg bieten, nutze ihn — ggf. als Bild-Crop oder in eigener Formulierung.

**Visuelle Unterstützung:** Wenn die Situation von einer Skizze, Grafik oder Darstellung profitiert, dann füge sie ein! Möglichkeiten:
- **Bild-Crop aus dem Buch** (bevorzugt): Viele Bücher liefern passende Abbildungen zur Einstiegssituation (z.B. Skizze einer Kugelstoßanlage, Schema eines Riesenrads). Diese als Bild mit `buchseite`-Angabe einfügen.
- **Koordinatensystem**: Wenn die Schüler Werte eintragen oder Graphen skizzieren sollen.
- **Tabelle**: Wenn die Schüler Werte berechnen und vergleichen sollen (z.B. Bogenlänge für verschiedene Radien → Muster entdecken).

Entscheide bei jeder Einstiegssituation: *Wäre es ohne Bild schwerer zu verstehen?* Wenn ja → Bild einfügen. Typische Fälle: geometrische Situationen, Versuchsaufbauten, räumliche Anordnungen, Graphen-Verläufe.

Gute Denkanstöße folgen einem dieser Muster:
- **Rechne mit Bekanntem → entdecke ein Muster**: z.B. Bogenlängen für verschiedene Radien berechnen, Quotienten bilden → „Was fällt auf?"
- **Alltagsproblem → Grenzen des Bekannten**: z.B. eine Situation, in der Grad-Angaben unpraktisch sind
- **Beobachte → formuliere eine Vermutung**: z.B. Messwerte vergleichen, Regelmäßigkeit erkennen

**Keine separate Überschrift „Denkanstoß"** auf der Seite einfügen. Der Phasenname „Einstieg" erscheint automatisch im Header-Kasten. Die Seite beginnt direkt mit der Situation oder Aufgabe.

### Phase 2: Erarbeitung (1–2 Seiten)
Gemeinsame Erarbeitung des neuen Themas an der Tafel/am Beamer:
- Ein konkretes Beispiel oder eine Rechnung durcharbeiten
- In Physik ggf. ein Experiment beschreiben/auswerten
- Neue Gesetzmäßigkeit, Regel oder Definition entwickeln
- Merksatz als Ergebnis der Erarbeitung formulieren

**Wichtig:** Viel Freiraum zum gemeinsamen Arbeiten. Die Seite soll wie ein Tafelbild aufgebaut sein — Arbeitsauftrag oben, darunter Platz zum Rechnen/Skizzieren, am Ende der Merksatz.

### Phase 3: Übungsaufgaben (1–2 Seiten)
Basisaufgaben aus dem Buch zum Üben:
- Direkte Anwendung des gerade Erarbeiteten
- Als Bild-Crops aus dem Buch einfügen
- Genug Freiraum nach jeder Aufgabe

### Phase 4: Vertiefungsaufgaben (1–2 Seiten)
Weiterführende Aufgaben aus dem Buch:
- Höheres Anforderungsniveau
- Transfer, Begründungen, komplexere Anwendungen
- Als Bild-Crops aus dem Buch einfügen
- Genug Freiraum nach jeder Aufgabe

## Mehrzyklische Struktur

Wenn die Buchseiten **mehrere aufeinander aufbauende Teilthemen** enthalten (z.B. erst Bogenmaß-Umrechnung, dann Sinus/Kosinus im Bogenmaß), wird die Stunde in **mehrere Zyklen** gegliedert. Jeder Zyklus durchläuft die vier Phasen:

```
Zyklus 1: Einstieg → Erarbeitung → Übung → Vertiefung
Zyklus 2: Einstieg → Erarbeitung → Übung → Vertiefung
(ggf. Zyklus 3: ...)
```

**Wann mehrere Zyklen?** Wenn die Buchseiten:
- Einen neuen Abschnitt mit eigener Überschrift oder eigenem Merksatz enthalten
- Neue Begriffe oder Konzepte einführen, die auf dem ersten Teil aufbauen
- Eigene Basisaufgaben und weiterführende Aufgaben zu einem Teilthema haben

**Wann KEIN neuer Zyklus?** Wenn die Aufgaben nur Variationen desselben Konzepts sind (z.B. verschiedene Schwierigkeitsgrade derselben Umrechnungsaufgabe).

Die .xopp-Datei darf dadurch **länger werden** — das ist gewollt. Sie wird dann über mehrere Unterrichtsstunden eingesetzt. Die Phasennamen im JSON werden durchnummeriert:

```json
"phasen": [
  {"name": "Einstieg", "inhalte": [...]},
  {"name": "Erarbeitung", "inhalte": [...]},
  {"name": "Übungsaufgaben", "inhalte": [...]},
  {"name": "Vertiefungsaufgaben", "inhalte": [...]},
  {"name": "Einstieg", "inhalte": [...]},
  {"name": "Erarbeitung", "inhalte": [...]},
  {"name": "Übungsaufgaben", "inhalte": [...]},
  {"name": "Vertiefungsaufgaben", "inhalte": [...]}
]
```

Nur der **erste** Einstieg bekommt den zweizeiligen Header mit Fach/Thema. Alle weiteren Einstiegsphasen bekommen den normalen Header.

## Ablauf – Schritt für Schritt

### Schritt 1: Buchseiten analysieren

Analysiere die hochgeladenen Bilder/PDFs:
- Welches Thema/Kapitel wird behandelt?
- **Wie lautet die Hauptüberschrift inkl. Kapitelnummer?** (z.B. "6.2 Sinusfunktion und Kosinusfunktion" → Dateiname)
- **Gibt es eine Einstiegssituation oder ein Sachbeispiel am Kapitelanfang?** (z.B. Kugelstoßanlage, Riesenrad — als mögliche Grundlage für den Denkanstoß!)
- Welche Definitionen, Merksätze, Beispiele sind vorhanden?
- Welche Aufgaben gibt es? (Nummern, Teilaufgaben, Schwierigkeitsgrad)
- Welche Aufgaben sind "Basisaufgaben" und welche "Weiterführende Aufgaben"?
- **Welche Seitenzahlen sind sichtbar?** (z.B. S. 180, S. 181 — diese werden bei den Aufgaben angegeben!)

**Fach und Jahrgangsstufe** aus dem Inhalt ableiten, falls nicht angegeben.

### Schritt 2: Denkanstoß entwickeln

**Zuerst im Buch schauen!** Prüfe, ob die Buchseiten bereits einen Einstieg bieten:
- Gibt es eine Einleitungssituation oder ein Sachbeispiel am Kapitelanfang? (z.B. Kugelstoßanlage, Riesenrad, Pendel)
- Gibt es eine Grafik oder Abbildung, die sich als Ausgangspunkt eignet?
- Gibt es eine Aufgabe mit dem Marker „Was fällt auf?" oder ähnlichem Entdeckungscharakter?

Wenn ja: Nutze diesen Einstieg — als Bild-Crop (mit `buchseite`) oder in eigener Formulierung.

**Falls das Buch keinen guten Einstieg bietet**, entwickle selbst einen, der diese Regeln befolgt:

1. **Nur Vorwissen voraussetzen**: Die Aufgabe muss mit dem lösbar sein, was die Schüler bereits können (Kreisumfang, Proportionalität, Dreisatz, etc.). Das neue Konzept darf **nicht** als bekannt vorausgesetzt werden.
2. **Zur Entdeckung führen**: Die Schüler sollen durch eigenes Rechnen auf ein Muster oder eine Beobachtung stoßen, die den Weg zum neuen Thema öffnet.
3. **Konkret statt abstrakt**: Zahlen, Situationen, Bilder — keine abstrakten Definitionen.
4. **Ohne separate Überschrift** — der Text beginnt direkt mit der Situation oder Aufgabe.

**Beispiel (schlecht):** „Ein Trainer sagt: Du bist 1 gelaufen. Was meint er?" → Schüler können nicht antworten, weil sie das Bogenmaß noch nicht kennen.

**Beispiel (gut):** „Berechne die Bogenlänge für α = 40° bei Radius 10 m, 15 m, 20 m und 25 m. Bilde jeweils den Quotienten Bogenlänge ÷ Radius. Was fällt dir auf?" → Schüler entdecken: Der Quotient ist immer gleich — das motiviert das Bogenmaß als neues Winkelmaß.

### Schritt 3: Erarbeitung planen

Plane die gemeinsame Erarbeitung:
- Wähle ein geeignetes Beispiel (ggf. aus dem Buch oder selbst entwickelt)
- Strukturiere den Weg von der Frage zum Merksatz
- Plane Arbeitsaufträge und Freiraum

### Schritt 4: Aufgaben auswählen und zuordnen

Wähle Aufgaben aus dem Buch:
- **Übungsaufgaben**: 2–4 Basisaufgaben (direkte Anwendung)
- **Vertiefungsaufgaben**: 2–3 weiterführende Aufgaben (Transfer, Begründung)

Die Auswahl sollte eine sinnvolle Progression bilden.

### Schritt 5: Buchausschnitte zuschneiden

Bildausschnitte aus dem Buch werden **nur für Aufgaben** eingefügt. Merksätze, Definitionen und Erklärungen formulierst du selbst als Text.

**Buchseite immer angeben!** Jeder Bild-Crop aus dem Buch bekommt das Feld `"buchseite": "S. XXX"`. Das Skript rendert die Seitenangabe automatisch als kleine graue Referenz über dem Bild. So wissen Schüler und Lehrkraft immer, wo die Aufgabe im Buch steht.

#### Pixelgenaues Zuschneiden

**Crop-Koordinaten nie schätzen.** Systematisch ermitteln:

1. **Bildgröße ermitteln** mit Python/PIL:
   ```python
   from PIL import Image
   img = Image.open("/mnt/user-data/uploads/buchseite.png")
   print(f"Bildgröße: {img.width}x{img.height}")
   ```

2. **Aufgabengrenzen finden**: Analysiere das Bild visuell (mit `view`-Tool) und bestimme für jede Aufgabe:
   - Obere Kante (Aufgabennummer)
   - Untere Kante (letzte Teilaufgabe/Grafik)
   - Linker und rechter Rand

3. **Sicherheitsabstände**: Mind. 10px oben, 15px unten, 5px links/rechts.

#### Goldene Regeln für Ausschnitte
- **Passgenau**: Genau die eine Aufgabe — nicht mehr, nicht weniger
- **Vollständig**: Aufgabennummer, alle Teilaufgaben, Hinweise, Skizzen
- **Nichts Fremdes**: Keine Teile anderer Aufgaben
- **Pro Aufgabe ein Bild**: Jede Aufgabe bekommt ihren eigenen Ausschnitt

### Schritt 6: Lösungen erstellen

**Immer Lösungen erstellen!** Zu jeder Stunde wird eine Lösungs-PDF für die Lehrkraft generiert. Die Lösungen kommen als `"loesungen"`-Feld in die plan.json.

Die Lösungen werden nach Phasen gegliedert:
```json
"loesungen": {
  "Einstieg (Denkanstoß)": [
    {"type": "text", "content": "Erwartete Antwort: ..."}
  ],
  "Erarbeitung": [
    {"type": "text", "content": "Beispielrechnung: ..."},
    {"type": "text", "content": "Merksatz-Ergebnis: ..."}
  ],
  "Übungsaufgaben": [
    {"type": "aufgabe", "nr": "1", "loesung": "a) 1,57  b) 0,79  c) 0,17 ..."},
    {"type": "aufgabe", "nr": "2", "loesung": "a) 30°  b) 240° ..."}
  ],
  "Vertiefungsaufgaben": [
    {"type": "aufgabe", "nr": "5", "loesung": "a) 0,79  b) 1,92 ..."}
  ]
}
```

Gib zu **jeder** Aufgabe und zu **jedem** Rechenbeispiel die vollständige Lösung an. Die PDF ist für die Lehrkraft gedacht — sie soll alle Ergebnisse auf einen Blick sehen können.

### Schritt 7: JSON-Plan erstellen und generieren

Lies `references/plan_schema.md` für die genaue JSON-Struktur.

Der Workflow:

```bash
SKILL_DIR="/pfad/zum/skill"

# 1. JSON-Plan erstellen (mit Python json.dump für korrektes Escaping)
#    → plan.json

# 2. Crop-Vorschau generieren und JEDEN Crop visuell prüfen
python3 "$SKILL_DIR/scripts/preview_crops.py" plan.json ./crop_previews
# → Jeden Crop mit view-Tool ansehen und prüfen
# → Bei Fehlern: plan.json korrigieren und erneut prüfen

# 3. Nach erfolgreicher Verifikation die .xopp erzeugen
python3 "$SKILL_DIR/scripts/generate_xopp.py" plan.json "<DATEINAME>.xopp"

# 4. Lösungs-PDF erzeugen
pip install fpdf2 --break-system-packages -q
python3 "$SKILL_DIR/scripts/generate_loesungen_pdf.py" plan.json "<DATEINAME>_Loesungen.pdf"
```

**Dateiname aus Kapitel-Überschrift ableiten:**
Kapitelnummer + Thema, z.B. `6.2_Sinusfunktion_und_Kosinusfunktion.xopp`.
- Leerzeichen → Unterstriche
- Umlaute beibehalten
- Sonderzeichen entfernen
- Lösungs-PDF: gleicher Name + `_Loesungen.pdf`

Kopiere beide Dateien nach `/mnt/user-data/outputs/`.

## Seitenlogik

Es gibt **keine** Vorbereitungsseite für die Lehrkraft und **keine** Lösungsseiten in der .xopp-Datei. Die .xopp besteht nur aus den vier Phasen, die direkt projiziert werden. Lösungen kommen in eine separate PDF.

Im JSON wird `"skip_vorbereitung": true` gesetzt, um die leere Vorbereitungsseite zu überspringen.

### Phasen-Mapping im JSON:
- **Denkanstoß** → Phasenname `"Einstieg"` (bekommt den Doppel-Header mit Fach/Thema)
- **Erarbeitung** → Phasenname `"Erarbeitung"`
- **Übungsaufgaben** → Phasenname `"Übungsaufgaben"`
- **Vertiefungsaufgaben** → Phasenname `"Vertiefungsaufgaben"`

### Kopfzeilen-Regeln
- **Seite 1 (Denkanstoß = "Einstieg")**: Zweizeiliger Header — Zeile 1: `Fach - Sequenzthema`, Zeile 2: `Stundenthema` + Phasenbox
- **Rechts oben immer**: `Dr. Winkelmann`
- **Weitere Seiten**: Phasenname im Header-Kasten

## Didaktische Hinweise

- Der **Denkanstoß** muss mit Vorwissen lösbar sein — das neue Konzept darf nicht vorausgesetzt werden. Bevorzugt den Buch-Einstieg nutzen, wenn einer vorhanden ist.
- Die **Erarbeitung** ist das Herzstück — hier wird gemeinsam gedacht und gerechnet
- **Übungsaufgaben** festigen das Gelernte
- **Vertiefungsaufgaben** fordern zum Transfer heraus
- Jede Schülerseite braucht großzügigen **Freiraum** (mind. 150px)

## Qualitätscheck vor Abgabe

1. ☐ Denkanstoß ist mit Vorwissen lösbar und führt zum neuen Thema hin (setzt das neue Konzept NICHT voraus)
2. ☐ Erarbeitung enthält konkretes Beispiel und Merksatz
3. ☐ Aufgaben korrekt aus dem Buch referenziert
4. ☐ **Buchseite bei jedem Bild-Crop angegeben** (Feld `buchseite`)
5. ☐ Genug Freiraum auf jeder Seite
6. ☐ **ALLE Bild-Crops mit preview_crops.py geprüft**
7. ☐ Kein Crop schneidet Text ab oder zeigt fremde Aufgaben
8. ☐ **Alle Texte verwenden echte Umlaute** (ä, ö, ü, ß)
9. ☐ **Keine Vorbereitungsseite** (`skip_vorbereitung: true`)
10. ☐ **Lösungs-PDF erzeugt** mit vollständigen Lösungen zu allen Phasen

## Wichtige Hinweise

- Die .xopp-Datei ist komprimiertes XML (gzip). Das Skript übernimmt die Komprimierung.
- Bilder werden als Base64 eingebettet.
- Der Nutzer öffnet die Datei in Xournal++ und projiziert sie am Beamer.
- Die Datei muss Seite für Seite durch den Unterricht führen.
- **Keine Vorbereitungsseite** — `skip_vorbereitung: true` setzen.
- **Keine Lösungsseiten in der .xopp** — Lösungen kommen in die separate PDF.
- **Keine Hausaufgaben-Phase** — endet mit den Vertiefungsaufgaben.
- **Lösungs-PDF immer mitliefern** — zu jeder .xopp gehört eine Lösungs-PDF.
