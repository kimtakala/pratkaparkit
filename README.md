# Prätkä-parkit

Prätkä-parkit on Flaskilla ja SQLitellä toteutettu web-sovellus moottoripyörien parkkipaikkojen tallentamiseen ja etsimiseen Suomessa. Sovellus noudattaa kurssin vaatimuksia: käyttöliittymä on toteutettu HTML- ja CSS-sivuilla, JavaScriptiä ei käytetä, eikä sovellus tarvitse Flaskin lisäksi muita asennettavia Python-kirjastoja.

## Keskeiset toiminnot

- Käyttäjärekisteröinti ja kirjautuminen
- Parkkipaikan lisääminen, muokkaaminen ja poistaminen (koordinaatit: lat, lon)
- Parkkipaikkojen listaus ja yksityiskohtanäkymä
- Haku (hakusana, osoite tai bounding-box lat/lon)
- Käyttäjäsivut: omat merkinnät ja perusstatistiikat
- Parkkipaikkojen luokittelu usealla luokalla
- Toissijainen tietokohde: kommentit parkkipaikkoihin liittyville huomautuksille
- Karttalinkki ja palvelinpuolinen staattinen laattakuvaesikatselu ilman JavaScriptiä

## Asennus

Sovellus toimii Python 3.10:ssa tai uudemmassa. Suositeltu tapa on käyttää virtuaaliympäristöä.

1. Kloonaa projekti ja siirry hakemistoon

```bash
git clone https://github.com/kimtakala/pratkaparkit.git
cd pratkaparkit
```

2. Varmista Python 3.10 tai uudempi

Varmista, että käytössä on Python 3.10 tai uudempi. Valitse käyttöjärjestelmäsi mukainen ohje:

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install -y python3.10 python3.10-venv
```

**Fedora/RHEL:**

```bash
sudo dnf install -y python3.10
```

**macOS (Homebrew):**

```bash
brew install python@3.10
```

**Windows:**
Lataa ja asenna Python 3.10 asennusohjelma viralliselta sivulta [python.org/downloads/windows](https://www.python.org/downloads/windows/). Muista ruksia asennusvaiheessa "Add Python 3.10 to PATH". Windowsilla komennot jatkossa ovat tyypillisesti `python` eikä `python3.10`.

3. Luo ja aktivoi virtuaaliympäristö

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
```

Jos `python --version` ei näytä vähintään versiota 3.10, luo virtuaaliympäristö uudelleen oikealla Python-komennolla.

Windowsilla tarvitset myös `tzdata`-paketin, jotta `zoneinfo` löytää `Europe/Helsinki`-aikavyöhykkeen.

4. Asenna riippuvuudet

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. Alusta tietokanta

```bash
sqlite3 database.db < sql/schema.sql
sqlite3 database.db < sql/init.sql
```

6. Käynnistä sovellus

```bash
python app.py
```

Jos haluat käyttää Flaskin komentoa, aseta ensin `FLASK_APP=app.py`.

```bash
export FLASK_APP=app.py
flask run
```

## Sovelluksen rakenne

- `app.py`: kaikki reitit, template-filtterit ja sovelluksen alustaminen
- `db.py`: tietokanta-apufunktiot ja yhteys SQLiteen
- `users.py`, `items.py`, `comments.py`: liiketoimintalogiikka
- `validation/`: lomakevalidoinnit
- `security/`: kirjautumisen ja CSRF:n apufunktiot
- `errors/`: virheenkäsittely
- `geo_helpers.py`: OpenStreetMapiin liittyvät apufunktiot
- `templates/`: Jinja2-sivupohjat, pohjana `layout.html`
- `static/main.css`: oma responsiivinen tyylitiedosto
- `sql/schema.sql`: tietokannan skeema
- `sql/init.sql`: alkudata ja luokittelut

## Testaus ja tarkistus

Automatisoidut testit löytyvät hakemistosta `tests/`. Ne voi ajaa komennolla:

```bash
python -m unittest discover -s tests
```

Testit kattavat kirjautumisen, validointivirheet, parkkipaikan luonnin, kommentoinnin, haun ja käyttäjäsivun peruspolut.

Sovelluksen lopullinen tila on testattu myös Pylintillä, ja raportti löytyy tiedostosta `PYLINT_REPORT.md`.

## Suuren tietomäärän testi

Sovellukselle on mukana erillinen `seed.py`-tiedosto, jolla voi luoda suuren testiaineiston tietokantaan. Se lisää käyttäjiä ja noin tuhat parkkipaikkaa, jotta sivutusta ja indeksejä voi testata käytännössä.

```bash
python seed.py
```

Suurta aineistoa varten sovellus käyttää sivutusta listauksessa ja haussa sekä indeksejä tietokannassa (`sql/schema.sql`).

## Koordinaattien lisääminen (ohje käyttäjälle)

Jos haluat lisätä tarkan sijainnin, avaa OpenStreetMap (https://www.openstreetmap.org), etsi sijainti ja käytä Share → Permalink tai kopioi koordinaatit (muoto `lat,lon`) ja liitä ne lomakkeeseen.

Esimerkki OSM-linkistä, joka avaa koordinaatin:

```
https://www.openstreetmap.org/?mlat=60.1695&mlon=24.9354#map=18/60.1695/24.9354
```

Voit myös liittää koordinaatit käsin ja käyttää karttaesikatselua nähdäksesi palvelinpuolisen staattisen laattakuvan (ei interaktiota).

## OpenStreetMap ja attribuutio

Map data © OpenStreetMap contributors

Muista asettaa `User-Agent` palvelinpuolisissa pyyntöjä varten, jos kutsut Nominatim- tai tile-palvelua.

## Työkalut ja rajaukset

- Sovellus käyttää ainoastaan Flaskia ja Pythonin standardikirjastoja (ei `requests`, ei JS-kirjastoja).
- Tietokantaa käytetään suorin SQL-komennoin (ei ORM:ia).
