def validate_lat_lon(lat_raw, lon_raw):
    try:
        lat = float(lat_raw)
        lon = float(lon_raw)
    except ValueError:
        return None, None, "Koordinaatit eivät ole numeroita."
    if not (59.0 <= lat <= 70.5):
        return None, None, "Vain Suomen koordinaatit sallittu (lat 59.0 ... 70.5)."
    if not (18.5 <= lon <= 32.0):
        return None, None, "Vain Suomen koordinaatit sallittu (lon 18.5 ... 32.0)."
    return lat, lon, None

def validate_spot_form(form):
    errors = []
    title = form.get("title", "").strip()
    if not title:
        errors.append("Otsikko puuttuu")

    lat, lon, err = validate_lat_lon(form.get("lat"), form.get("lon"))
    if err:
        errors.append(err)

    data = {
        "title": title,
        "description": form.get("description", "").strip(),
        "lat": lat,
        "lon": lon,
        "address": form.get("address", "").strip(),
        "tags": form.get("tags", "").strip()
    }
    return data, errors
