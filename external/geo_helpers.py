"""Helpers for geolocation and OpenStreetMap tile preview using only standard library."""

import math
import json
import urllib.parse
import urllib.request


def deg2num(lat, lon, zoom):
    """Convert latitude/longitude to OSM tile numbers."""
    lat_rad = math.radians(float(lat))
    n = 2.0 ** int(zoom)
    xtile = int((float(lon) + 180.0) / 360.0 * n)
    ytile = int(
        (1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n
    )
    return xtile, ytile


def tile_url(lat, lon, zoom=15):
    """Return a public OSM tile URL for given lat/lon at zoom level."""
    x, y = deg2num(lat, lon, zoom)
    return f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"


def nominatim_lookup(address, email=None):
    """Query Nominatim (OSM) for an address and return first result's lat/lon.

    Uses Python standard library. Respect Nominatim usage policy: set a descriptive User-Agent
    (include email if possible) and avoid heavy usage.
    """
    base = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
    }
    url = base + "?" + urllib.parse.urlencode(params)
    ua = "PratkaParkit/1.0"
    if email:
        ua += f" ({email})"
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = resp.read().decode("utf-8")
    results = json.loads(data)
    if not results:
        return None
    r = results[0]
    return float(r["lat"]), float(r["lon"])
