# Xournal++ Unterrichtsplaner – Automatische Stundenerstellung

## Zweck dieses Repos
Dieses Repository dient der automatischen Erstellung von Xournal++-Unterrichtsdateien (.xopp) auf Basis von Schulbuchseiten (Bilder/PDFs).

## Skill-Zuordnung nach Fach

Je nach Fach wird ein anderer Skill verwendet:

| Fach | Skill | Verzeichnis | Beschreibung |
|------|-------|-------------|--------------|
| **Mathe** | xournal-minimal | `skills/xournal-minimal/` | Kompakte 4-Phasen-Struktur (Denkanstoß, Erarbeitung, Übung, Vertiefung). Keine Lehrerseite, keine Hausaufgaben, Lösungen als separate PDF. |
| **Physik** | xournal-unterricht | `skills/xournal-unterricht/` | Vollständige 90-Minuten-Stunde mit Lehrerseite, allen Phasen (Einstieg, Erarbeitung, Sicherung, Übung, Hausaufgabe, Reserve), Lösungen am Ende der .xopp. |

**Standardverhalten:**
- **Mathe-Stunde** → immer `xournal-minimal`, wenn nicht anders gefordert
- **Physik-Stunde** → immer `xournal-unterricht`, wenn nicht anders gefordert
- Der Nutzer kann jederzeit explizit den anderen Skill anfordern (z. B. "erstelle eine ausführliche Mathe-Stunde" → xournal-unterricht)

## Automatischer Workflow

Wenn der Nutzer ein Bild oder PDF einer Schulbuchseite schickt (ohne weitere Anweisungen), dann:

1. **Analysiere den Anhang** und extrahiere:
   - Fach (Mathe oder Physik)
   - Kapitel-/Abschnittsnummer und Titel (z. B. "6.1 Baumdiagramme")
   - Sequenzthema (z. B. "Mehrstufige Zufallsexperimente")
   - Klassenstufe (falls erkennbar, sonst fragen)
   - Buchseiten und Aufgabennummern
   - Alle Aufgaben, Beispiele, Definitionen, Merksätze, Abbildungen

2. **Wähle den passenden Skill** anhand des Fachs (siehe Tabelle oben).

3. **Lies die SKILL.md** des gewählten Skills (`skills/<skill-name>/SKILL.md`) und befolge die dortigen Anweisungen vollständig.

4. **Erstelle die .xopp-Datei** mit dem `generate_xopp.py`-Skript des gewählten Skills:
   ```bash
   SKILL_DIR="skills/<skill-name>"
   python3 "$SKILL_DIR/scripts/generate_xopp.py" plan.json "<Dateiname>.xopp"
   ```

5. **Speichere die Datei** im Ordner:
   ```
   <Fach>/<Klasse>/<Sequenzthema>/<Abschnittsnummer + Titel>.xopp
   ```
   Beispiel: `Mathe/8G/Mehrstufige Zufallsexperimente/6.1 Baumdiagramme.xopp`

6. **Committe und pushe** die Änderungen.

## Hinweise zur Ordnerstruktur
- Fach: `Mathe` oder `Physik`
- Klasse: z. B. `8G`, `7A`, `10B` – falls nicht erkennbar, nachfragen
- Sequenzthema: aus der Kapitelüberschrift des Buchs ableiten
- Dateiname: Abschnittsnummer + Titel aus dem Anhang

## Skill-Verzeichnisstruktur

Jeder Skill ist vollständig unter `skills/<skill-name>/` abgelegt:

```
skills/
├── xournal-minimal/
│   ├── SKILL.md                    # Skill-Anweisungen (4-Phasen-Modell)
│   ├── references/plan_schema.md   # JSON-Schema für den Plan
│   ├── scripts/generate_xopp.py    # .xopp-Generator
│   ├── scripts/preview_crops.py    # Crop-Vorschau
│   ├── scripts/generate_loesungen_pdf.py  # Lösungs-PDF-Generator
│   └── assets/template_unterricht-xournal.xopp  # Template
│
└── xournal-unterricht/
    ├── SKILL.md                    # Skill-Anweisungen (90-Min-Stunde)
    ├── references/plan_schema.md   # JSON-Schema für den Plan
    ├── scripts/generate_xopp.py    # .xopp-Generator
    ├── scripts/preview_crops.py    # Crop-Vorschau
    └── assets/template_unterricht-xournal.xopp  # Template
```

## Standardannahmen (wenn nicht anders angegeben)
- Klasse: Nachfragen, wenn nicht erkennbar
- Mathe: Kompakte Stunde (xournal-minimal)
- Physik: Vollständige Doppelstunde 90 Minuten (xournal-unterricht)
- Kopfzeile rechts oben: "Dr. Winkelmann"
