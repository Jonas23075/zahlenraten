# Zahlenraten

Ein einfaches, barrierefreies Zahlenspiel als Flask-Webanwendung.

---

## 🚀 Kurzbeschreibung

**Zahlenraten** ist ein kleines Flask-Projekt, bei dem sich die Applikation eine Zahl zwischen 1 und 100 ausdenkt und Spieler*innen diese erraten. Die Anzahl der Versuche wird gespeichert und in einer Highscore-Liste angezeigt.

Das Projekt eignet sich als Lernprojekt für Webentwicklung mit Python/Flask, Session-Handling, SQLite und grundlegender Web-Security.

---

## 🔧 Technologien & Struktur

* **Python 3.13.9**
* **Flask** (Web-Framework)
* **SQLite** (eingebettete DB)
* **HTML / CSS / JS** (Templates unter `flaskr/templates`)
* **Blueprints** zur Modularisierung

Projektstruktur (Auszug):

```
zahlenraten/
├─ flaskr/
│  ├─ static/
|  |  ├─ css/
|  |  ├─ styles.css
|  |  ├─ js/
|  |  └game.js
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ index.html
│  │  ├─ login.html
│  │  ├─ register.html
│  │  └ scores.html
│  ├─ __init__.py
│  ├─ auth.py
│  ├─ game.py
│  ├─ scores.py
│  ├─ db.py
│  ├─ security.py
│  └─ templates/
├─ instance/
│  └zahlenspiel.db
├─ tests/
│  ├─ test_auth.py
│  ├─ test_game.py
│  ├─ conftest.py
│  ├─ test_db.py
│  └─ test_scores.py
├─ app.py
├─ pyproject.toml
├─ .gitignore
├─ requirements.txt
└─ README.md
```

---

## 🎯 Features

* Session-basiertes Login/Logout
* Zahlenspiel (1–100) mit Feedback: „zu hoch“ / „zu niedrig"
* Speicherung von Versuchen und Users in SQLite
* Highscore-Tabelle
* Unit-Tests mit pytest
* Fokus auf Barrierefreiheit und Security-Hardening

---

## ✅ Installation & Start

**1) Repository klonen**

```bash
git clone <DEIN_REPO_URL>
cd zahlenraten
```

**2) Virtuelle Umgebung erstellen**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**3) Abhängigkeiten installieren**

```bash
pip install -r requirements.txt
```

**4) Datenbank initialisieren**

```bash
flask init-db
```

**5) Server starten**

```bash
flask run --debug
```

[Zahlenraten öffnen](http://127.0.0.1:5000/).

---

## 🕹️ Spielanleitung

1. Einloggen oder direkten Benutzernamen beim Spielen angeben.
2. Das Spiel wählt zufällig eine Zahl (1–100).
3. Gib Tipps ab; die App meldet „zu hoch“ / „zu niedrig“.
4. Bei richtigem Tipp wird die Anzahl der Versuche gespeichert und in die Highscore-Liste aufgenommen.

---

## ⚙️ Tests

Unit-Tests mit pytest:

```bash
python -m pytest tests/ -v
```

Schreibe Tests für die Kernfunktionen: DB-Operationen, Auth, Spiel-Logik und API-Endpunkte.

---

## ♿ Barrierefreiheit (Accessibility) — Quick-Check

> Diese Liste ist als Arbeits- und Prüf-Liste gedacht. Hake Punkte im Projekt ab und dokumentiere Abweichungen im Issue-Tracker.

* [ ] HTML `lang` gesetzt (`<html lang="de">`)
* [ ] Semantische Überschriften (H1..H6) in logischer Reihenfolge
* [ ] Alle Bilder haben sinnvolle `alt`-Attribute
* [ ] Formulare besitzen eindeutige `<label>`-Elemente
* [ ] Fokuszustände sichtbar (`:focus`) und gut erfassbar
* [ ] Alle interaktiven Elemente per Tastatur erreichbar (Tab-Reihenfolge prüfen)
* [ ] Skip-Link zum Hauptinhalt vorhanden (`<a href="#main" class="skip-link">`)
* [ ] Farben und Kontraste prüfen (Text:Hintergrund >= 4.5:1 für normalen Text)
* [ ] Informationen nicht ausschließlich über Farbe kommuniziert
* [ ] Videos/Audio: Untertitel oder Transkript verfügbar
* [ ] Animierte Inhalte: Abschaltoption
* [ ] ARIA-Rollen und `aria-live` für dynamische Inhalte korrekt verwendet
* [ ] Modale Dialoge: `aria-modal="true"` und korrektes Fokus-Management
* [ ] Fehlermeldungen semantisch und für Screenreader zugänglich
* [ ] Screenreader-Tests (z. B. NVDA / VoiceOver) dokumentiert
* [ ] Lighthouse / axe DevTools Audit durchführen und Issues tracken

---

## 🔒 Sicherheit — Penetrationstest-Quick-Checks

> Diese Tests sind einfache Manuelles-Checks. Führe sie in einer sicheren Testumgebung aus und dokumentiere Ergebnisse.

1. **SQL Injection (SQLi)**

   * Test: Auf Login-Seite `username: ' OR '1'='1` eingeben.
   * Erwartet: Login darf **nicht** funktionieren.
   * Abhilfe: Prepared Statements / parametrisierte Queries (z. B. `sqlite3` mit Platzhaltern) oder ORM (SQLAlchemy).

    ![alt text](pics/66fe6e708247e973ce51af96_608958ea27293628afb3b58b_SQL_20injection_20work.jpeg)

2. **Cross-Site Scripting (XSS)**

   * Test: Benutzername `&lt;script&gt;alert('XSS')&lt;/script&gt;` registrieren und Highscores prüfen.
   * Erwartet: Script darf nicht ausgeführt werden.
   * Abhilfe: Output escapen (Jinja2 escaped standardmäßig) und Eingaben validieren.

    ![alt text](pics/XSS_Attack.svg)

3. **Cross-Site Request Forgery (CSRF)**

   * Test: Externe HTML-Form mit POST zur App abschicken.
   * Erwartet: Requests ohne CSRF-Token abweisen.
   * Abhilfe: CSRF-Schutz (z. B. Flask-WTF oder eigene Token-Implementierung).

    ![alt text](pics/what-is-cross-site-request-forgery.png)

4. **Session Management**

   * Test: Session-Cookie kopieren und in anderem Client einsetzen.
   * Erwartet: Session darf nicht ohne Authentifizierung nutzbar sein.
   * Abhilfe: Starker `SECRET_KEY`, `session.permanent` und Cookie-Eigenschaften (`HttpOnly`, `Secure` auf HTTPS).

    ![alt text](pics/What_is_a_session.webp)

5. **Directory Traversal**

   * Test: Pfad-Manipulationen wie `../../../etc/passwd` versuchen.
   * Erwartet: Keine unautorisierte Datei-Auslesung.
   * Abhilfe: Pfad-Normalisierung und Whitelisting; niemals Nutzereingaben direkt in Dateipfade übernehmen.

---
