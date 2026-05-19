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

Kurssiohjeen mukaan sovellus tehdään Python 3.10.x -ympäristössä. Tämä versio lukitaan projektiin tiedostolla [.python-version](.python-version), joten kehitysympäristön pitää käyttää juuri 3.10-sarjaa eikä esimerkiksi 3.11:ta.

1. Kloonaa projekti ja siirry hakemistoon

```bash
git clone https://github.com/kimtakala/pratkaparkit
cd pratkaparkit
```

2. Varmista Python-versio

```bash
python3 --version
```

Varmista, että tulos on 3.10.x. Jos koneella on useita Python-versioita, käytä nimenomaan Python 3.10:ä.

3. Luo ja aktivoi virtuaaliymparisto

```bash
python3 -m venv venv
source venv/bin/activate
python --version
```

Jos `python --version` ei näytä 3.10.x:ää, poista venv ja luo se uudelleen oikealla Python 3.10 -tulkilla, esimerkiksi komennolla `python3.10 -m venv venv`.

4. Asenna riippuvuudet

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. Alusta tietokanta

```bash
sqlite3 database.db < sql/init_db.sql
```

6. Kaynnista sovellus

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Versionhallinta (että pysyy kunnossa)

Projektissa ei pideta versionhallinnassa valiaikaistiedostoja. Tarkista ennen commitia:

```bash
git status
```

Varmista erityisesti, etteivat seuraavat paady Git-historiaan:

- venv/
- .env
- database.db
- .local/
- **pycache**/
- .python-version

Huomaa, että `requirements.txt` kuuluu versioonhallintaan, koska siihen listataan projektin Python-riippuvuudet.

Tyypillinen paivitysrunko:

```bash
git add .
git commit -m "Implement <feature>"
git push
```

Commit-viestit kirjoitetaan englanniksi.

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
