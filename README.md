# Zahlenraten

## Beschreibung

Zahlenraten ist ein kleines Flask Projekt, bei dem sich die ein Randomizer eine Zahl zwischen 1 und 100 ausdenkt und der Nutzer diese erraten muss. Die Anzahl der Versuche wird gespeichert und in einer Highscore-Liste angezeigt.

## Technologien & Struktur

* **Python > 3.x**
* **Flask**
* **SQLite**
* **HTML / CSS / JS**
* **Blueprints**

Projektstruktur (Filesystem (Tree)):

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

## Features

* Session Login/Logout
* Zahlenspiel (1–100)
* Speicherung von Versuchen und Users in SQLite
* Highscore speicherung
* Unit-Tests mit pytest
* Barrierefreiheit und Web-Security

---

## Installation & Start

**1) Repository klonen**

```bash
git clone git@github.com:Jonas23075/zahlenraten.git
cd zahlenraten
```

**2) Virtuelle Umgebung erstellen**

Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
**Linux**/~~Mac~~
```bash
python3 -m venv .venv
source ./.venv/bin/activate
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

[Zahlenraten öffnen](http://127.0.0.1:5000/)

---

## Spielanleitung

1. Einloggen oder direkten Benutzernamen beim Spielen angeben.
2. Das Spiel wählt zufällig eine Zahl (1–100).
3. Gib Tipps ab; die App meldet „zu hoch“ / „zu niedrig“.
4. Bei richtigem Tipp wird die Anzahl der Versuche gespeichert und in die Highscore-Liste aufgenommen.

---

## Tests

Unit-Tests mit pytest:

```bash
python -m pytest tests/ -v
```

Testergebnisse:
```bash
tests/test_auth.py::test_register PASSED
tests/test_auth.py::test_register_existing_user PASSED
tests/test_auth.py::test_login PASSED
tests/test_auth.py::test_logout PASSED
tests/test_auth.py::test_load_logged_in_user PASSED
tests/test_db.py::test_get_close_db PASSED
tests/test_db.py::test_init_db_command PASSED
tests/test_game.py::test_game_get PASSED
tests/test_game.py::test_game_guess_too_low PASSED
tests/test_game.py::test_game_guess_too_high PASSED
tests/test_game.py::test_game_guess_correct PASSED
tests/test_game.py::test_game_invalid_guess PASSED 
tests/test_scores.py::test_highscores PASSED   
```

---

## Barrierefreiheit

* [x] HTML `lang` gesetzt (`<html lang="de">`)
* [x] Semantische Überschriften (H1..H6) in logischer Reihenfolge
* [x] Alle Bilder haben sinnvolle `alt`-Attribute
* [x] Formulare besitzen eindeutige `<label>`-Elemente
* [x] Fokuszustände sichtbar (`:focus`) und gut erfassbar
* [x] Alle interaktiven Elemente per Tastatur erreichbar (Tab-Reihenfolge prüfen)
* [x] Skip-Link zum Hauptinhalt vorhanden (`<a href="#main" class="skip-link">`)
* [x] Farben und Kontraste prüfen (Text:Hintergrund >= 4.5:1 für normalen Text)
* [x] Informationen nicht ausschließlich über Farbe kommuniziert
* [x] Videos/Audio: Untertitel oder Transkript verfügbar
* [x] Animierte Inhalte: Abschaltoption
* [x] ARIA-Rollen und `aria-live` für dynamische Inhalte korrekt verwendet
* [x] Modale Dialoge: `aria-modal="true"` und korrektes Fokus-Management
* [x] Fehlermeldungen semantisch und für Screenreader zugänglich
* [x] Screenreader-Tests (z. B. NVDA / VoiceOver) dokumentiert
* [x] Lighthouse / axe DevTools Audit durchführen und Issues tracken

---

## Sicherheit — Penetrationstest-Quick-Checks

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
