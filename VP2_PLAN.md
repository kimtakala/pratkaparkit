# VP2 Plan - Pratka-parkit

Tavoite: toteuttaa valipalautus 2 niin, etta sovelluksessa on toimiva minimitaso
kurssivaatimusten mukaisesti.

## Rajaus VP2:een

- Paatietokohde: parking_spot (sijainti)
- Toissijainen tietokohde: comment
- Ei kayteta report-rakennetta.

Huomio: kurssin VP2-vaatimuksissa toissijainen tietokohde ei ole viela pakollinen,
mutta se pidetaan mukana rakenteessa valipalautus 3:a varten.

## VP2-vaatimuskohtainen toteutussuunnitelma

1. Kayttajatunnus ja kirjautuminen

- Rekisterointi: username + password (hashattu tallennus)
- Login/logout session-pohjaisesti
- Kayttooikeustarkistus reiteille, jotka vaativat kirjautumisen

2. Parking spot CRUD

- Luo uusi parking spot: title, description, lat, lon, address, tags
- Muokkaa omaa parking_spotia
- Poista oma parking_spot
- Omistajuuden tarkistus muokkaus- ja poistoreiteissa

3. Listaus

- Etusivulle lista uusimmista parking_spoteista (myos muiden)
- Yksityiskohtasivu yhdelle parking_spotille

4. Haku

- Tekstihaku title/description/address/tags
- Sijaintihaku bounding box -ehdoilla (lat/lon min/max)
- Parametrisoidut SQL-kyselyt kaikkiin hakuihin

## Tietokantarakenne (VP2)

Taulut:

- users
- parking_spot
- comment

Comment-taulu pidetaan yksinkertaisena:

- id
- parking_spot_id (FK -> parking_spot.id)
- author_id (FK -> users.id)
- text
- created_at

## Reittisuunnitelma (app.py)

- GET / : parking_spot-listaus
- GET /register, POST /register
- GET /login, POST /login
- POST /logout
- GET /spots/new, POST /spots/new
- GET /spots/<id>
- GET /spots/<id>/edit, POST /spots/<id>/edit
- POST /spots/<id>/delete
- GET /search

Commentit voidaan lisata jo VP2:ssa yksityiskohtasivulle:

- POST /spots/<id>/comments/new

## Turvallisuuslista

- CSRF-token kaikissa POST-lomakkeissa
- Parametrisoidut SQL-kyselyt
- Syotevalidointi: lat [-90, 90], lon [-180, 180]
- Oikeustarkistus: muokkaus/poisto vain omiin kohteisiin
- Salasanat hashattuina

## Tyojarjestys

1. Luo app-runko ja DB-yhteysmoduuli
2. Toteuta auth (register/login/logout)
3. Toteuta parking_spot CRUD
4. Toteuta listaus + yksityiskohta (hyodyntaen `examples/geo_helpers.py` staattista laattakuvaesikatselua)
5. Toteuta haku (teksti + bbox)
6. Lisaa comment-lomake yksityiskohtasivulle
7. Toteuta HTML/CSS-frontend ilman JavaScriptia (kurssin perusvaatimusten mukaisesti)
8. Testaa VP2-vaatimukset kasin ja paivita README

## Hyvaksyntakriteerit VP2:lle

- Uusi kayttaja pystyy rekisteroitymaan ja kirjautumaan
- Kirjautunut kayttaja pystyy lisaamaan, muokkaamaan ja poistamaan oman spotin
- Kaikki kayttajat nakyvat listauksessa ja yksityiskohtasivu toimii
- Hakutoiminto palauttaa tuloksia tekstilla tai koordinaattirajauksella
- Sovellus kaynnistyy puhtaasta kloonista README-ohjeella
