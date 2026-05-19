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

## Asennus ja käynnistys

Varmista, että käytät Python 3.10 -ympäristöä (tai vastaavaa).

```bash
python -m venv venv
source venv/bin/activate
pip install Flask
```

Alusta tietokanta `sql/init_db.sql` avulla:

```bash
sqlite3 database.db < sql/init_db.sql
```

Käynnistä sovellus (esimerkinomainen):

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

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

## Seuraavat askeleet

- Täydennä `app.py` (reitit, lomakkeet, login) kurssin esimerkkien pohjalta.
- Lisää frontend-sivut HTML/CSS:llä ilman JS:ää.
- Lisää tarvittaessa staattinen laattakuvaesikatselu `examples/geo_helpers.py`-funktion avulla.
