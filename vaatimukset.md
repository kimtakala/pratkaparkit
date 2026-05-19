# Moottoripyörä Parkki — Projektikohtaiset vaatimukset

Tämä dokumentti selventää, miten kurssin yleisvaatimukset soveltuvat projektiin "Moottoripyörä Parkki".

## Yleistä

- Sovellus toteutetaan Pythonilla ja Flaskilla.
- Tiedot tallennetaan SQLite-tietokantaan.
- Sovellus ei käytä JavaScriptiä eikä muita erikseen asennettavia Python-kirjastoja.
- OpenStreetMapia voidaan hyödyntää: geokoodaus Nominatim-palvelua tai staattisia laattakuvia, mutta kaikki kutsut tehdään palvelinpuolelta käyttäen Pythonin standardikirjastoja ja asetettu `User-Agent`.
- Näytä näkyvä attribuutio: "Map data © OpenStreetMap contributors".

## Perusvaatimusten vastaavuus

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään — `users`-taulu ja kirjautumisreitit.
- Käyttäjä voi lisätä, muokata ja poistaa `parking_spot`-tietueita (sisältää `lat`,`lon`).
- Käyttäjä näkee sekä omat että muiden lisäämät parkkipaikat listauksessa.
- Haku hakusanalla tai rajaamalla koordinaattien avulla (bounding box).
- Käyttäjäsivut näyttävät tilastoja ja käyttäjän lisäämät parkkipaikat.
- Luokittelu (tags) tallennetaan tietokantaan ja liitetään parkkipaikkoihin.
- Toissijainen tietokohde: `report`/`comment` parkkipaikkojen lisätiedoille.

## Kartta- ja sijaintiratkaisut ilman JavaScriptiä

- Käyttäjä voi lisätä tarkan sijainnin liittämällä koordinaatit manuaalisesti OSM:stä.
- Vaihtoehtoisesti sovellus tarjoaa palvelinpuolisen staattisen tile-esikatselun `<img>`-tagilla.
- Geokoodaus (osoite → koordinaatit) tehdään palvelinpuolelta Nominatimilla tarvittaessa.

## Turvallisuus ja hyvä käytäntö

- Käytä CSRF-suojausta lomakkeissa.
- Parametrisoidut SQL-kyselyt.
- Validointi: lat ∈ [-90,90], lon ∈ [-180,180].

## Dokumentaatio

- README_moottoripyora.md sisältää projektikuvauksen, asennusohjeet ja ohjeet koordinaattien lisäämiseen.
- Lisää `sql/init_db.sql` ja ohjeet tietokannan luonnista README:hen.
