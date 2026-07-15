"""Validation helpers for parking spot forms."""

import re

_DMS_PATTERN = re.compile(
    r"^\s*(?P<degrees>\d+(?:\.\d+)?)\s*(?:°|deg)?\s*"
    r"(?P<minutes>\d+(?:\.\d+)?)?\s*(?:'|′|’|m)?\s*"
    r"(?P<seconds>\d+(?:\.\d+)?)?\s*(?:\"|″|”|s)?\s*"
    r"(?P<hemisphere>[NSEW])?\s*$",
    re.IGNORECASE,
)


def _parse_coordinate(raw_value, axis):
    """Parse a coordinate value in decimal or DMS form."""

    if raw_value is None:
        return None, "Koordinaatti puuttuu."

    text = str(raw_value).strip()
    if not text:
        return None, "Koordinaatti puuttuu."

    try:
        return float(text), None
    except ValueError:
        pass

    match = _DMS_PATTERN.match(text)
    if not match:
        return None, "Koordinaatti ei ole kelvollisessa muodossa."

    degrees = float(match.group("degrees"))
    minutes = float(match.group("minutes") or 0)
    seconds = float(match.group("seconds") or 0)
    hemisphere = (match.group("hemisphere") or "").upper()

    if minutes >= 60 or seconds >= 60:
        return None, "Koordinaatti ei ole kelvollisessa muodossa."

    decimal = degrees + (minutes / 60) + (seconds / 3600)

    if hemisphere in {"S", "W"}:
        decimal = -decimal

    error = None
    if hemisphere and axis == "lat" and hemisphere not in {"N", "S"}:
        error = "Leveysasteessa pitää käyttää N tai S -kirjainta."
    elif hemisphere and axis == "lon" and hemisphere not in {"E", "W"}:
        error = "Pituusasteessa pitää käyttää E tai W -kirjainta."

    return (None, error) if error else (decimal, None)


def validate_lat_lon(lat_raw, lon_raw):
    """Validate latitude and longitude values and return parsed floats."""

    lat, lat_err = _parse_coordinate(lat_raw, "lat")
    if lat_err:
        return None, None, f"Leveysaste: {lat_err}"

    lon, lon_err = _parse_coordinate(lon_raw, "lon")
    if lon_err:
        return None, None, f"Pituusaste: {lon_err}"

    if not 59.0 <= lat <= 70.5:
        return None, None, "Leveysasteen pitää olla välillä 59.0 ... 70.5."
    if not 18.5 <= lon <= 32.0:
        return None, None, "Pituusasteen pitää olla välillä 18.5 ... 32.0."
    return lat, lon, None


def validate_spot_form(form):
    """Validate the parking spot form and return cleaned data."""

    errors = []
    title = form.get("title", "").strip()
    if not title:
        errors.append("Otsikko puuttuu.")

    lat, lon, err = validate_lat_lon(form.get("lat"), form.get("lon"))
    if err:
        errors.append(err)

    data = {
        "title": title,
        "description": form.get("description", "").strip(),
        "lat": lat,
        "lon": lon,
        "address": form.get("address", "").strip(),
        "tags": form.get("tags", "").strip(),
    }
    return data, errors
