# Zahlenraten
Ein Projekt in Flask

## 🔧 Technologien & Struktur

- **Python**
- **Flask** (Web-Framework)
- **SQLite** (Datenbank)
- **HTML / CSS** (Templates unter `flaskr/templates`)
- **JS**
- **Blueprints** für klare Projektstruktur


## 🚀 Installation & Start

### 1) Repository klonen
```bash
git clone <dein-repo-link>
cd zahlenspiel
````

### 2) Virtuelle Umgebung erstellen

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

### 3) Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4) Datenbank initialisieren

```bash
flask --app flaskr init-db
```

### 5) Server starten

```bash
flask --app flaskr run --debug
```

Die Anwendung läuft jetzt unter:

```
http://127.0.0.1:5000/
```

---

## 🎮 Spielprinzip

1. **Einloggen** (oder direkt ein Benutzername beim Spielen eingeben)
2. Das Spiel denkt sich eine Zahl zwischen **1 und 100** aus.
3. Du gibst Tipps ab — das Spiel sagt *zu hoch* oder *zu niedrig*.
4. Sobald du richtig liegst ⏱️ → Anzahl der Versuche wird gespeichert.
5. Deine Ergebnisse erscheinen in der **Highscore-Tabelle**.

---

## 📝 Features

| Feature          | Beschreibung                                   |
| ---------------- | ---------------------------------------------- |
| Login / Logout   | Session-basierte einfache Anmeldung            |
| Zahlenspiel      | Zufallszahl mit Feedback („höher“/„niedriger“) |
| Highscore-Liste  | Speicherung der Spielstände in SQLite          |
| Saubere Struktur | Nutzung von Flask Blueprints                   |

---

## ✅ To-Do / Weiterentwicklung

* Benutzerverwaltung mit Passwort-Hashing
* Schwierigkeitsgrade hinzufügen
* Grafisches UI oder Animationen
* API-Endpunkte für Scores


---
