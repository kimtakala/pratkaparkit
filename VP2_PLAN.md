\*\*\*\*# VP2 Plan - Prätkä-parkit

Tavoite: toteuttaa välipalautus 2 niin, että sovelluksessa on toimiva minimitaso
kurssivaatimusten mukaisesti.

## Rajaus VP2:een

- Päätietokohde: parking_spot (sijainti)
- Toissijainen tietokohde: comment
- Ei käytetä report-rakennetta.

Huomio: kurssin VP2-vaatimuksissa toissijainen tietokohde ei ole vielä pakollinen,
mutta se pidetään mukana rakenteessa välipalautus 3:a varten.

## VP2-vaatimuskohtainen toteutussuunnitelma

1. Käyttäjätunnus ja kirjautuminen

- Rekisteröinti: username + password (hashattu tallennus)
- Login/logout session-pohjaisesti
- Käyttöoikeustarkistus reiteille, jotka vaativat kirjautumisen

2. Parking spot CRUD

- Luo uusi parking spot: title, description, lat, lon, address, tags
- Muokkaa omaa parking_spotia
- Poista oma parking_spot
- Omistajuuden tarkistus muokkaus- ja poistoreiteissa

3. Listaus

- Etusivulle lista uusimmista parking_spoteista (myös muiden)
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

Comment-taulu pidetään yksinkertaisena:

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

Commentit voidaan lisätä jo VP2:ssa yksityiskohtasivulle:

- POST /spots/<id>/comments/new

## Turvallisuuslista

- CSRF-token kaikissa POST-lomakkeissa
- Parametrisoidut SQL-kyselyt
- Syötevalidointi (Suomen rajat): lat [59.0, 70.5], lon [18.5, 32.0]
- Oikeustarkistus: muokkaus/poisto vain omiin kohteisiin
- Salasanat hashattuina

## Työjärjestys

1. Luo app-runko ja DB-yhteysmoduuli
2. Toteuta auth (register/login/logout)
3. Toteuta parking_spot CRUD
4. Toteuta listaus + yksityiskohta (hyödyntäen `examples/geo_helpers.py` staattista laattakuvaesikatselua)
5. Toteuta haku (teksti + bbox)
6. Lisaa comment-lomake yksityiskohtasivulle
7. Toteuta HTML/CSS-frontend ilman JavaScriptia (kurssin perusvaatimusten mukaisesti)
8. Testaa VP2-vaatimukset kasin ja päivitä README

## Hyväksyntäkriteerit VP2:lle

- Uusi käyttäjä pystyy rekisteröitymään ja kirjautumaan
- Kirjautunut käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan oman spotin
- Kaikki käyttäjät näkyvät listauksessa ja yksityiskohtasivu toimii
- Hakutoiminto palauttaa tuloksia tekstillä tai koordinaattirajauksella
- Sovellus käynnistyy puhtaasta kloonista README-ohjeella
