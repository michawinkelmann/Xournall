# Xournal++ Unterrichtsplaner – Automatische Stundenerstellung

## Zweck dieses Repos
Dieses Repository dient der automatischen Erstellung von Xournal++-Unterrichtsdateien (.xopp) auf Basis von Schulbuchseiten (Bilder/PDFs).

## Automatischer Workflow

Wenn der Nutzer ein Bild oder PDF einer Schulbuchseite schickt (ohne weitere Anweisungen), dann:

1. **Analysiere den Anhang** und extrahiere:
   - Fach (Mathe oder Physik)
   - Kapitel-/Abschnittsnummer und Titel (z. B. "6.1 Baumdiagramme")
   - Sequenzthema (z. B. "Mehrstufige Zufallsexperimente")
   - Klassenstufe (falls erkennbar, sonst fragen)
   - Buchseiten und Aufgabennummern
   - Alle Aufgaben, Beispiele, Definitionen, Merksätze, Abbildungen

2. **Erstelle die .xopp-Datei** nach den Regeln in `skill.txt` und dem Layout aus `template_unterricht-xournal.xopp`.

3. **Speichere die Datei** im Ordner:
   ```
   <Fach>/<Klasse>/<Sequenzthema>/<Abschnittsnummer + Titel>.xopp
   ```
   Beispiel: `Mathe/8G/Mehrstufige Zufallsexperimente/6.1 Baumdiagramme.xopp`

4. **Committe und pushe** die Änderungen.

## Hinweise zur Ordnerstruktur
- Fach: `Mathe` oder `Physik`
- Klasse: z. B. `8G`, `7A`, `10B` – falls nicht erkennbar, nachfragen
- Sequenzthema: aus der Kapitelüberschrift des Buchs ableiten
- Dateiname: Abschnittsnummer + Titel aus dem Anhang

## Hinweise zur .xopp-Erstellung
- Die kompletten Regeln stehen in `skill.txt`
- Das Template `template_unterricht-xournal.xopp` definiert Layout und Stil
- Die .xopp-Datei ist gzip-komprimiertes XML (Xournal++-Format)
- Erstelle das XML, dann komprimiere es mit gzip zu .xopp

## Standardannahmen (wenn nicht anders angegeben)
- Klasse: Nachfragen, wenn nicht erkennbar
- Doppelstunde: 90 Minuten
- Kopfzeile rechts oben: "Dr. Winkelmann"
