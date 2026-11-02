"""
Downloads the poster photos from Wikimedia Commons into marketing/photos/ and
records the credit line each licence requires in photos/credits.json.

    python3 marketing/fetch_photos.py
"""
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "photos")
UA = {"User-Agent": "YatraPosterBot/1.0 (Hare Krishna Golden Temple Hyderabad; mkcd@hkmhyderabad.org)"}

# key: (Commons file title, short label, width)
PHOTOS = {
    "towerbridge": ("File:Tower Bridge golden hour.jpg", "Tower Bridge", 1920),
    "manor": ("File:Bhaktivedanta Manor - 01.JPG", "Bhaktivedanta Manor", 960),
    "eiffel": ("File:Paris - The Eiffel Tower in spring - 2307.jpg", "Eiffel Tower", 960),
    "keukenhof": ("File:Keukenhof 2018 DSC 0059.jpg", "Keukenhof", 960),
    "titlis": ("File:Titlis-1.jpg", "Titlis", 960),
    "venice": ("File:Gondolas, Grand Canal, Venice.jpg", "Venice", 960),
    "colosseum": ("File:Colosseum of Rome, Italy.jpg", "Colosseum", 960),
    "windmills": ("File:Windmills at Zaanse Schans, Zaanstad, 2022.jpg", "Zaanse Schans", 960),
    "amsterdam": ("File:Colorful canal houses at golden hour in Damrak avenue Amsterdam the Netherlands.jpg", "Amsterdam", 960),
    "rhinefalls": ("File:Neuhausen am Rheinfall.jpg", "Rhine Falls", 960),
    "lucerne": ("File:Luzern - Chapel Bridge - March 2019 (02).jpg", "Lucerne", 960),
    "pisa": ("File:The Duomo and Tower of Pisa at sunrise.jpg", "Pisa", 960),
    "westminster": (None, "Westminster", 960),
    "radhadesh": (None, "Radhadesh", 960),
    "vatican": (None, "St Peter's", 960),
}


def get(url, binary=False):
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                data = r.read()
                return data if binary else json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(20 * (attempt + 1))
    raise RuntimeError("rate limited: " + url)


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def main(overrides=None):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "credits.json")
    credits = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    for key, (title, label, width) in PHOTOS.items():
        title = (overrides or {}).get(key, title)
        if not title or (key in credits and credits[key]["title"] == title):
            continue
        q = urllib.parse.urlencode({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata",
                                    "iiurlwidth": width, "format": "json", "formatversion": 2})
        page = get("https://commons.wikimedia.org/w/api.php?" + q)["query"]["pages"][0]
        ii = page["imageinfo"][0]
        meta = ii.get("extmetadata", {})
        fname = key + ".jpg"
        with open(os.path.join(OUT, fname), "wb") as f:
            f.write(get(ii.get("thumburl") or ii["url"], binary=True))
        credits[key] = {"file": fname, "title": title, "label": label, "source": ii["descriptionurl"],
                        "artist": strip(meta.get("Artist", {}).get("value")) or "unknown",
                        "license": strip(meta.get("LicenseShortName", {}).get("value"))}
        print(key, credits[key]["artist"], credits[key]["license"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(credits, f, ensure_ascii=False, indent=1)
        time.sleep(6)


if __name__ == "__main__":
    import sys
    main(dict(a.split("=", 1) for a in sys.argv[1:]))
