# Prätkä-parkit

Prätkä-parkit on yksinkertainen web-sovellus, jonka avulla käyttäjät voivat lisätä ja löytää moottoripyörien parkkipaikkoja Suomessa. Sovellus noudattaa kurssin vaatimuksia: se on toteutettu Pythonilla ja Flaskilla, käyttää SQLite-tietokantaa, eikä se vaadi JavaScriptiä tai muita ulkopuolisia Python-kirjastoja.

## Keskeiset toiminnot

- Käyttäjärekisteröinti ja kirjautuminen
- Parkkipaikan lisääminen, muokkaaminen ja poistaminen (koordinaatit: lat, lon)
- Parkkipaikkojen listaus ja yksityiskohtanäkymä
- Haku (hakusana, osoite tai bounding-box lat/lon)
- Käyttäjäsivut: omat merkinnät ja perusstatistiikat
- Toissijainen tietokohde: `comment` parkkipaikkoihin liittyville huomautuksille
- Karttanäkymä ilman JavaScriptiä: suora linkki OpenStreetMapiin ja/tai palvelinpuolinen staattinen laattakuvaesikatselu

## Kehitysympäristön pystytys (venv + Git)

Kurssiohjeen mukaan sovellus tehdään Python 3.10 tai uudempi -ympäristössä. Projektissa käytetään virtuaaliympäristöä, eikä sovellus vaadi muita Python-kirjastoja kuin ne, jotka löytyvät `requirements.txt`-tiedostosta.

1. Kloonaa projekti ja siirry hakemistoon

```bash
git clone https://github.com/kimtakala/pratkaparkit.git
cd pratkaparkit
```

2. Asenna tai varmista Python 3.10 tai uudempi

Varmista, että koneeltasi löytyy Python 3.10 tai uudempi. Valitse käyttöjärjestelmäsi mukainen ohje:

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

Jos `python --version` ei näytä vähintään 3.10.x:ää, poista venv ja luo se uudelleen oikealla Python-komennolla.

4. Asenna riippuvuudet

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. Alusta tietokanta

```bash
sqlite3 database.db < sql/init_db.sql
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

- `app.py`: kaikki reitit ja sovelluksen alustaminen
- `db/__init__.py`: tietokanta-apufunktiot
- `users.py`, `items.py`, `comments.py`: liiketoimintalogiikka
- `validation/`: lomakevalidoinnit
- `templates/`: Jinja2-sivupohjat
- `static/main.css`: oma responsiivinen tyylitiedosto
- `sql/init_db.sql`: tietokannan alustus

## Testaus ja tarkistus

Automatisoidut testit löytyvät hakemistosta `tests/`. Ne voi ajaa komennolla:

```bash
python -m unittest discover -s tests
```

Tee lisäksi nämä manuaaliset tarkistukset ennen palautusta:

1. Käynnistä sovellus.
2. Rekisteröi käyttäjä.
3. Kirjaudu sisään.
4. Lisää parkkipaikka.
5. Avaa parkkipaikan yksityiskohta.
6. Lisää kommentti.
7. Kokeile hakua ja bounding-box-hakua.
8. Avaa käyttäjäsivu.

## Koordinaattien lisääminen (ohje käyttäjälle)

Jos haluat lisätä tarkan sijainnin, avaa OpenStreetMap (https://www.openstreetmap.org), etsi sijainti ja käytä Share → Permalink tai kopioi koordinaatit (muoto `lat,lon`) ja liitä ne lomakkeeseen.

Esimerkki OSM-linkistä, joka avaa koordinaatin:

```
https://www.openstreetmap.org/?mlat=60.1695&mlon=24.9354#map=18/60.1695/24.9354
```

Voit myös liittää koordinaatit käsin ja napsauttaa "Näytä esikatselu" nähdäksesi palvelinpuolisen staattisen laattakuvan (ei interaktiota).

## OpenStreetMap ja attribuutio

Map data © OpenStreetMap contributors

Muista asettaa `User-Agent` palvelinpuolisissa pyyntöjä varten, jos kutsut Nominatim- tai tile-palvelua.

## Työkalut ja rajaukset

- Sovellus käyttää ainoastaan Flaskia ja Pythonin standardikirjastoja (ei `requests`, ei JS-kirjastoja).
- Tietokantaa käytetään suorin SQL-komennoin (ei ORM:ia).
