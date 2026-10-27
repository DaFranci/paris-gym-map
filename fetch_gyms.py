"""Download all gyms in Île-de-France from OpenStreetMap and save them to data.js.

Run this whenever you want fresher data:  python fetch_gyms.py
"""
import json
import math
import re
import time
import unicodedata
import urllib.parse
import urllib.request

# Gyms are tagged inconsistently in OSM: many chain clubs (e.g. Les Cercles de la Forme)
# are leisure=sports_centre + sport=fitness rather than leisure=fitness_centre.
QUERY = ('[out:json][timeout:120];area["ISO3166-2"="FR-IDF"]->.a;('
         'nwr["leisure"="fitness_centre"](area.a);'
         'nwr["leisure"="sports_centre"]["sport"~"fitness|crossfit|weightlifting|bodybuilding"](area.a);'
         'nwr["amenity"="gym"](area.a);'
         ');out center tags;')
DUPLICATE_METRES = 60  # same name this close together = same gym mapped twice
ENDPOINTS = ['https://overpass-api.de/api/interpreter',
             'https://overpass.kumi.systems/api/interpreter']
KEEP_TAGS = ['name', 'brand', 'addr:housenumber', 'addr:street', 'addr:postcode', 'addr:city',
             'opening_hours', 'website', 'contact:website']


def fetch():
    body = urllib.parse.urlencode({'data': QUERY}).encode()
    for url in ENDPOINTS:
        try:
            req = urllib.request.Request(url, data=body, headers={'User-Agent': 'paris-gym-map/1.0'})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)['elements']
        except Exception as e:
            print(f'{url} failed: {e}')
    raise SystemExit('All Overpass servers failed, try again later.')


def simple_name(g):
    """Name ignoring case, accents and punctuation: "Le Dôme" == "Le Dome"."""
    s = unicodedata.normalize('NFD', g['tags'].get('brand') or g['tags'].get('name') or '')
    return re.sub(r'[^a-z0-9]', '', s.encode('ascii', 'ignore').decode().lower())


def dedupe(gyms):
    kept = []
    # Entries with more details (address, website...) first, so they're the ones kept.
    for g in sorted(gyms, key=lambda g: -len(g['tags'])):
        name = simple_name(g)
        if name and any(name == simple_name(k) and distance_m(g, k) < DUPLICATE_METRES for k in kept):
            continue
        kept.append(g)
    return kept


def distance_m(a, b):
    dy = (a['lat'] - b['lat']) * 111_320
    dx = (a['lon'] - b['lon']) * 111_320 * math.cos(math.radians(a['lat']))
    return math.hypot(dx, dy)


def main():
    gyms = []
    for e in fetch():
        lat = e.get('lat', e.get('center', {}).get('lat'))
        lon = e.get('lon', e.get('center', {}).get('lon'))
        if lat is None:
            continue
        tags = {k: v for k, v in e.get('tags', {}).items() if k in KEEP_TAGS}
        gyms.append({'lat': round(lat, 6), 'lon': round(lon, 6), 'id': f"{e['type']}/{e['id']}", 'tags': tags})
    gyms = dedupe(gyms)
    data = {'t': int(time.time() * 1000), 'gyms': gyms}
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write('window.GYM_DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n')
    print(f'Saved {len(gyms)} gyms to data.js')


if __name__ == '__main__':
    main()
