---
name: xournal-unterricht
description: Erstellt fertige Xournal++ Unterrichtsdateien (.xopp) für Mathe und Physik aus Schulbuchseiten. Verwende diesen Skill immer, wenn der Nutzer Buchseiten (Bilder/PDF) hochlädt und daraus eine Unterrichtsstunde, ein Tafelbild, eine .xopp-Datei oder eine Unterrichtsvorbereitung erstellen möchte. Triggert auch bei Begriffen wie 'Unterricht planen', 'Stunde vorbereiten', '.xopp erstellen', 'Tafelbild', 'Xournal', 'Unterrichtsentwurf aus Buch', 'Buchseiten für den Unterricht aufbereiten', oder wenn Lehrkräfte Bilder von Schulbuchseiten hochladen und eine fertige Unterrichtsdatei erwarten. Auch relevant wenn jemand eine 90-Minuten-Stunde, Doppelstunde oder Unterrichtsplanung auf Basis von Lehrbuchmaterial wünscht.
---

# Xournal++ Unterrichtsplaner

Du erstellst auf Basis hochgeladener Schulbuchseiten eine fertige, projizierbare Xournal++-Datei (.xopp) für eine 90-Minuten-Unterrichtsstunde.

## Deine Rolle

Du bist Mathematik-/Physiklehrer (Sek I/II), professioneller Didaktiker und Unterrichtsplaner. Du analysierst die Buchseiten, planst eine didaktisch hochwertige Stunde und lieferst eine fertige .xopp-Datei, die ohne Nacharbeit am Beamer einsetzbar ist.

**Sprache: Immer korrekte deutsche Umlaute verwenden!**
Alle Texte in der .xopp-Datei (Vorbereitung, Aufgaben, Merksätze, Lösungen — alles) müssen echte deutsche Umlaute und Sonderzeichen verwenden: **ä, ö, ü, Ä, Ö, Ü, ß**. Schreibe niemals Ersatzformen wie ae, oe, ue, ss. Das gilt auch für den JSON-Plan: Verwende `json.dump(..., ensure_ascii=False)`, damit Umlaute korrekt als UTF-8 geschrieben werden.

## Ablauf – Schritt für Schritt

### Schritt 1: Informationen sammeln

Frage den Nutzer nach fehlenden Infos (sofern nicht schon bekannt):
- **Fach**: Mathematik oder Physik
- **Jahrgangsstufe**: z.B. Klasse 8, Q1
- **Besonderheiten**: Vorwissen, Lerngruppe, besondere Wünsche

Falls der Nutzer nur Buchseiten hochlädt ohne weitere Infos: Triff plausible Annahmen (Fach aus Inhalt ablesen, Jahrgang schätzen) und notiere diese auf Seite 1.

### Schritt 2: Buchseiten analysieren

Analysiere die hochgeladenen Bilder/PDFs gründlich:
- Welches Thema/Kapitel wird behandelt?
- **Wie lautet die Hauptüberschrift auf der Seite, inklusive Kapitelnummer?** (z.B. "6.2 Wahrscheinlichkeiten bei Baumdiagrammen" – Nummer und Titel werden als Dateiname für die .xopp-Datei verwendet!)
- Welche Definitionen, Merksätze, Beispiele sind vorhanden?
- Welche Aufgaben gibt es? (Nummern, Teilaufgaben, Schwierigkeitsgrad)
- Welche Abbildungen/Grafiken sind enthalten?
- Welche Seitenzahlen sind sichtbar?

Wichtig: Erfinde keine Buchseiten oder Aufgabennummern. Nur das verwenden, was wirklich auf den Bildern steht.

### Schritt 3: Unterrichtsstunde planen

Entwirf einen 90-Minuten-Verlaufsplan mit folgender Phasenstruktur:

| Phase | ca. Minuten | Inhalt |
|-------|-------------|--------|
| Einstieg | 10-15 | Aktivierend, problemorientiert, Leitfrage |
| Erarbeitung I | 15-20 | Schrittweise Herleitung/Entdeckung |
| Sicherung | 10-15 | Fertiger Merksatz + Beispiel |
| Erarbeitung II / Übungen Basis | 15-20 | Aufgaben mit Buchbezug, Pflicht |
| Übungen weiterführend | 10-15 | Differenzierung, Challenge |
| Hausaufgabe | 5 | Aufgaben als Bild/Text zeigen + Seitenverweis |
| Reserve | — | Zusatzaufgaben/Vertiefung |

Du darfst Phasen anpassen, zusammenlegen oder ergänzen – die Stunde muss als 90-Minuten-Einheit realistisch durchführbar bleiben.

### Schritt 4: Buchausschnitte zuschneiden und einbetten

Bildausschnitte aus dem Buch werden **nur für Aufgaben** eingefügt — also für Übungen, die die Schüler bearbeiten sollen. Alles andere schreibst du selbst als Text/Merksatz.

#### Was wird als Bild eingefügt?
- **JA**: Aufgaben aus dem Buch (mit Aufgabennummer, allen Teilaufgaben, Hinweisen, Skizzen)
- **JA**: Abbildungen/Grafiken, die zu einer Aufgabe gehören und nicht als Text darstellbar sind
- **JA**: **Hausaufgaben-Aufgaben** — auch Aufgaben, die als Hausaufgabe aufgegeben werden, müssen als Bild-Crop (oder als Text-Fallback) auf der Hausaufgaben-Seite erscheinen, damit die SuS die Aufgabenstellung direkt sehen können, ohne das Buch aufschlagen zu müssen
- **NEIN**: Merksätze/Wissensboxen → stattdessen als `merksatz`-Element selbst formulieren
- **NEIN**: Definitionen, Erklärungstexte → stattdessen als `text`-Element selbst formulieren
- **NEIN**: Beispiele mit Lösungen → stattdessen selbst als Text aufschreiben oder in Lösungsseiten

Grund: Wenn du einen Merksatz sowohl als Bild einfügst als auch als Text schreibst, ist das redundant und unübersichtlich. Schreibe Inhalte, die du sowieso formulierst, immer nur als Text.

**Wichtig zur Hausaufgabe:** Eine bloße Angabe wie "S. 184, Nr. 12" reicht nicht aus. Die SuS fotografieren die Hausaufgaben-Seite ab oder schauen zu Hause nochmal drauf — wenn die Aufgabenstellung dort direkt sichtbar ist, können sie sofort loslegen. Füge daher für jede Hausaufgabe entweder einen Bild-Crop der Aufgabe aus dem Buch ein oder formuliere die Aufgabe als Text nach (Fallback, wenn kein passendes Bild vorliegt).

**Freiraum bei Hausaufgaben:** Nach jeder Hausaufgaben-Aufgabe muss ein großzügiger `freiraum` (mind. 200px Höhe) eingefügt werden, damit die SuS ihren Rechenweg und die Lösung direkt auf der projizierten Seite sehen und eintragen können. Behandle die Hausaufgaben-Seite genauso wie eine Übungsseite — Aufgabe + Platz zum Arbeiten gehören zusammen.

#### Pixelgenaues Zuschneiden

**WICHTIG: Crop-Koordinaten dürfen nie geschätzt werden.** Bestimme sie systematisch über eine Bildanalyse-Pipeline.

##### Schritt 4a: Bildgröße und Aufgabenpositionen exakt ermitteln

1. **Bildgröße ermitteln** mit Python/PIL:
   ```python
   from PIL import Image
   img = Image.open("/mnt/user-data/uploads/buchseite.png")
   print(f"Bildgröße: {img.width}x{img.height}")
   ```

2. **Aufgabengrenzen systematisch finden**: Analysiere das Bild, um die vertikale Position jeder Aufgabe zu bestimmen. Nutze das `view`-Tool, um das hochgeladene Bild visuell zu inspizieren, und bestimme die Grenzen jeder Aufgabe durch sorgfältige visuelle Analyse:
   - Wo beginnt die Aufgabennummer (obere Kante)?
   - Wo endet die letzte Teilaufgabe oder zugehörige Grafik (untere Kante)?
   - Welcher horizontale Bereich wird benötigt (linke/rechte Kante)?
   
3. **Aufgabenstruktur kartieren**: Erstelle vor dem JSON eine vollständige Karte aller Aufgaben mit ihren geschätzten Pixelpositionen. Notiere dir für jede Aufgabe:
   ```
   Aufgabe 1: top ~50px, bottom ~270px  (mit Grafik, braucht viel Platz)
   Aufgabe 2: top ~275px, bottom ~420px (nur Text, weniger Platz)
   Aufgabe 3: top ~425px, bottom ~500px (kurz, eine Zeile + Teilaufgaben)
   ```

4. **Sicherheitsabstände einplanen**:
   - Obere Kante: Mindestens 10px ÜBER der Aufgabennummer
   - Untere Kante: Mindestens 15px UNTER der letzten Zeile/Grafik der Aufgabe
   - Abstand zu Nachbar-Aufgaben: Der Crop darf KEINE Pixel einer anderen Aufgabe enthalten

##### Schritt 4b: Crop-Koordinaten angeben

**Immer Pixel-Koordinaten verwenden** (genauer als Prozentwerte):
```json
{
  "type": "bild",
  "path": "/mnt/user-data/uploads/buchseite.png",
  "crop": {"left_px": 988, "top_px": 50, "right_px": 1500, "bottom_px": 270}
}
```

Alternativ Prozentwerte (Dezimalstellen erlaubt):
```json
{
  "crop": {"left": 51.5, "top": 4.0, "right": 78.0, "bottom": 21.0}
}
```

#### Goldene Regeln für Ausschnitte

- **Passgenau**: Der Ausschnitt soll genau die eine Aufgabe zeigen — nicht mehr, nicht weniger
- **Nichts abschneiden**: Die Aufgabennummer, alle Teilaufgaben (a, b, c...), Hinweise am Rand, zugehörige Skizzen/Grafiken müssen komplett sichtbar sein. Prüfe insbesondere:
  - Hat die Aufgabe eine zugehörige Grafik/Foto am rechten Rand? → right_px weit genug setzen!
  - Gibt es Teilaufgaben a), b), c)? → bottom_px muss ALLE Teilaufgaben einschließen!
  - Gibt es eine Randbemerkung (z.B. "Stolperstelle", Hinweis)? → Diese muss mit rein!
- **Nichts Fremdes**: Keine Teile anderer Aufgaben, keine Überschriften fremder Abschnitte
- **Puffer**: Ca. 10–15px Rand oben/unten und 5px links/rechts
- **Pro Aufgabe ein Bild**: Jede einzelne Aufgabe bekommt ihren eigenen, passgenauen Ausschnitt

#### Systematisches Vorgehen bei Doppelseiten

Bei einem Foto/Scan von zwei Buchseiten nebeneinander (typisch ~1920x1280px):

```
|<------ Linke Seite ------>|<------ Rechte Seite ----->|
0px                       ~960px                     1919px  (horizontal)
|  Kopfzeile/Seitenzahl    |  Kopfzeile/Seitenzahl     |
|  Überschrift Abschnitt   |  Überschrift "Basisaufg."  |
|  Einführungstext          |  Aufg. 1  (mit Grafik)    |
|  Wissensbox/Definition    |  Aufg. 2  (mit Grafik)    |
|  Beispiel 1               |  Aufg. 3                  |
|  ...                      |  "Weiterführende Aufg."   |
|  Grafisches Lösen         |  Aufg. 4, 5, 6, ...       |
100%                                                     (vertikal)
```

**Beachte**: Aufgaben auf Buchseiten enthalten oft zugehörige Grafiken (Fotos, Skizzen, Diagramme) am rechten Rand. Der Crop muss diese IMMER mit einschließen. Setze `right_px` im Zweifel lieber bis zum Seitenrand (bei rechter Seite: bis ~1900px).

### Schritt 4c: Crops VERIFIZIEREN (Pflicht!)

**Dieser Schritt ist nicht optional.** Nachdem du plan.json erstellt hast, führe das Vorschau-Skript aus:

```bash
SKILL_DIR="/pfad/zum/skill"
python3 "$SKILL_DIR/scripts/preview_crops.py" plan.json ./crop_previews
```

Das Skript extrahiert jeden einzelnen Crop als PNG-Datei. Danach **musst** du jeden Crop mit dem `view`-Tool visuell prüfen:

```bash
# Jeden Crop einzeln ansehen:
view ./crop_previews/crop_01_Übungen_I_-_Basis.png
view ./crop_previews/crop_02_Übungen_I_-_Basis.png
# usw.
```

**Prüfe bei jedem Crop:**
1. ☐ Ist die Aufgabennummer komplett sichtbar? (nicht abgeschnitten oben)
2. ☐ Sind ALLE Teilaufgaben (a, b, c...) komplett sichtbar? (nicht abgeschnitten unten)
3. ☐ Sind zugehörige Grafiken/Fotos vollständig sichtbar? (nicht abgeschnitten rechts)
4. ☐ Ist KEIN Text einer anderen Aufgabe sichtbar? (kein Überhang oben/unten)
5. ☐ Sind keine abgeschnittenen Textzeilen am Rand sichtbar?

**Wenn ein Crop fehlerhaft ist:**
1. Korrigiere die Crop-Koordinaten in plan.json (mit `str_replace`)
2. Führe preview_crops.py erneut aus
3. Prüfe den korrigierten Crop erneut mit `view`
4. Wiederhole bis ALLE Crops sauber sind

**Erst wenn alle Crops verifiziert sind**, gehe zu Schritt 5 weiter.

### Schritt 5: JSON-Plan erstellen und .xopp generieren

Lies `references/plan_schema.md` für die genaue JSON-Struktur.

**Wichtig: Umlaute im JSON-Plan!** Alle Textinhalte im JSON müssen echte deutsche Umlaute enthalten (ä, ö, ü, ß) — niemals Ersatzschreibungen (ae, oe, ue, ss). Erstelle den JSON-Plan immer mit `json.dump(..., ensure_ascii=False, indent=2)` in Python, damit Umlaute korrekt als UTF-8 erhalten bleiben.

Der vollständige Workflow ist:

```bash
SKILL_DIR="/pfad/zum/skill"

# 1. JSON-Plan erstellen (mit Python json.dump für korrekte Escaping)
#    → plan.json

# 2. Crop-Vorschau generieren und JEDEN Crop visuell prüfen
python3 "$SKILL_DIR/scripts/preview_crops.py" plan.json ./crop_previews
# → Jeden Crop mit view-Tool ansehen und prüfen
# → Bei Fehlern: plan.json korrigieren und erneut prüfen

# 3. Erst nach erfolgreicher Verifikation die .xopp erzeugen
#    DATEINAME: Verwende die Hauptüberschrift/das Thema aus dem hochgeladenen
#    Anhang als Dateinamen. Sonderzeichen und Leerzeichen ersetzen (siehe unten).
python3 "$SKILL_DIR/scripts/generate_xopp.py" plan.json "<DATEINAME>.xopp"
```

**Dateiname aus Anhang-Überschrift ableiten:**
Ermittle die Hauptüberschrift (z.B. Kapitelüberschrift, Thementitel) aus dem vom Nutzer hochgeladenen Anhang (Buchseite/PDF). **Die Kapitelnummer (z.B. "6.2", "3.1", "4.5") muss immer im Dateinamen enthalten sein**, sofern sie auf der Buchseite angegeben ist. Die Nummer steht typischerweise direkt vor der Überschrift (z.B. "6.2 Wahrscheinlichkeiten bei Baumdiagrammen"). Verwende die vollständige Überschrift inklusive Nummer als Dateinamen. Dabei:
- Kapitelnummer immer voranstellen, z.B. `6.2_Wahrscheinlichkeiten_bei_Baumdiagrammen.xopp`
- Leerzeichen durch Unterstriche `_` ersetzen
- Umlaute beibehalten (ä, ö, ü, ß sind OK)
- Sonderzeichen entfernen (nur Buchstaben, Ziffern, Unterstriche, Bindestriche, Punkte in der Kapitelnummer)
- Dateiendung `.xopp` anhängen
- Beispiel: Überschrift "6.2 Wahrscheinlichkeiten bei Baumdiagrammen" → `6.2_Wahrscheinlichkeiten_bei_Baumdiagrammen.xopp`
- Beispiel: Überschrift "3.1 Kräfte und ihre Wirkungen" → `3.1_Kräfte_und_ihre_Wirkungen.xopp`
- Beispiel: Überschrift "Lineare Gleichungen mit zwei Variablen" (ohne Nummer) → `Lineare_Gleichungen_mit_zwei_Variablen.xopp`

Kopiere das Ergebnis nach `/mnt/user-data/outputs/`.

**Wichtig: Seitenumbruch und Ränder**
Das Skript hat automatischen Seitenumbruch eingebaut. Wenn der Inhalt einer Phase nicht auf eine Seite passt, wird automatisch eine Fortsetzungsseite erstellt. Trotzdem solltest du darauf achten:
- Packe nicht zu viele Elemente in eine Phase — lieber auf mehrere Phasen aufteilen
- Freiraum wird automatisch verkleinert wenn nötig, aber plane realistisch
- Bilder werden proportional skaliert und auf die Inhaltsbreite begrenzt
- Kein Element ragt jemals über den rechten oder unteren Seitenrand hinaus

## Seitenlogik: Was kommt wohin?

### Seite 1: Nur Lehrkraft (nicht projizieren)
Der `vorbereitung`-Text muss enthalten:
- Lernziele/Kompetenzen (inhaltlich + prozessbezogen)
- Einordnung in die Sequenz (Vorwissen, Anschluss, Ausblick)
- Minutengenauer Verlaufsplan mit Sozialformen (EA/PA/GA/Plenum)
- Material/Medien/Organisation
- Didaktische Hinweise: Kernidee, typische Fehlvorstellungen, Differenzierung
- Diagnosefragen (Woran erkenne ich Verständnis?)
- Reserve-Optionen
- Falls Annahmen getroffen wurden: diese hier notieren
- **Keine** Schüleraufträge oder Musterlösungen auf Seite 1

### Ab Seite 2: Schülerseiten (projizierbar)
Jede Phase bekommt mindestens eine eigene Seite mit:
- Klare Phasenüberschrift
- Kurze, eindeutige Arbeitsaufträge (nummeriert, imperativisch)
- Sozialformhinweis wenn nötig
- **Viel Freiraum** zum Rechnen, Skizzieren, Begründen
- Buchausschnitte an der passenden Stelle

### Letzte Seite(n): Lösungen (nur Lehrkraft)
- Vollständige Musterlösungen zu allen Aufgaben
- Erwartete Ergebnisse
- Typische Fehler + Lehrerimpulse
- Optional: Tafelbild-Endzustand

## Didaktische Qualitätskriterien

- **Einstieg aktivierend**: Ein Problem, Phänomen oder eine Frage, die neugierig macht
- **Leitfrage sichtbar**: Auf der Einstiegsseite klar formuliert
- **Merksatz in Sicherung**: Muss fertig formuliert auf der Seite stehen (als `merksatz`-Element)
- **Aufgabenprogression**: Vom Einfachen zum Komplexen
- **Differenzierung**: Pflicht + Zusatz/Challenge bei Übungen
- **Buchbezug**: Aufgaben mit Seitenzahl und Nummer referenzieren
- **Freiraum**: Jede Schülerseite braucht Platz. Nutze `freiraum`-Elemente großzügig (mind. 150px Höhe)

## Vorlagen nutzen

Je nach Thema passende leere Vorlagen einbauen:
- `koordinatensystem` für Graphen, Geraden, Funktionen
- `tabelle` für Wertetabellen, Messwerte, Rechenschritte
- `freiraum` für freies Rechnen/Skizzieren

Alle Vorlagen müssen leer und groß genug zum gemeinsamen Ausfüllen sein.

## Kopfzeilen-Regeln

- **Seite 1 + 2**: Zweizeiliger Header — Zeile 1: `Fach - Sequenzthema`, Zeile 2: `Stundenthema` (wird automatisch vom Skript aus den JSON-Feldern `fach`, `sequenzthema` und `stundenthema` erzeugt)
- **Rechts oben immer**: `Dr. Winkelmann` (wird automatisch vom Skript gesetzt)
- **Weitere Seiten**: Phasenname im Header-Kasten

## Qualitätscheck vor Abgabe

Prüfe vor dem Erstellen der .xopp:
1. ☐ Zeitplan (90 Min) ist plausibel und steht auf Seite 1
2. ☐ Einstieg ist aktivierend/problemorientiert
3. ☐ Sicherung enthält fertigen Merksatz
4. ☐ Buchaufgaben korrekt referenziert (Seite + Nr.)
5. ☐ Genug Freiraum auf jeder Schülerseite
6. ☐ Lösungen nur auf den letzten Seiten
7. ☐ **ALLE Bild-Crops mit preview_crops.py extrahiert und mit view-Tool visuell geprüft**
8. ☐ Kein Crop schneidet Aufgabentext, Teilaufgaben oder Grafiken ab
9. ☐ Kein Crop enthält Teile von Nachbar-Aufgaben
10. ☐ **Hausaufgabe enthält die Aufgabenstellungen** als Bild-Crop oder Text (nicht nur Seitenzahl + Nr.)
11. ☐ **Alle Texte verwenden echte Umlaute** (ä, ö, ü, ß) — keine Ersatzschreibungen (ae, oe, ue, ss)

## Wichtige Hinweise

- **Immer echte deutsche Umlaute verwenden** (ä, ö, ü, Ä, Ö, Ü, ß) in allen Texten — niemals ae, oe, ue, ss als Ersatz. Dies gilt für Vorbereitung, Aufgaben, Merksätze, Lösungen, Phasennamen und alle anderen Textfelder im JSON-Plan.
- Die .xopp-Datei ist komprimiertes XML (gzip). Das Skript übernimmt die Komprimierung.
- Bilder werden als Base64 eingebettet – die Datei kann dadurch groß werden, das ist normal.
- Der Nutzer öffnet die Datei in Xournal++ und projiziert sie am Beamer.
- Die Datei muss "wie ein Drehbuch" funktionieren: Seite für Seite durch den Unterricht führen.
