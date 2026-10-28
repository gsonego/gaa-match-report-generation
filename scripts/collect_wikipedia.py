"""Step 1 of the Wikipedia collection: download the raw wikitext of each
All-Ireland SFC season page and record its revision id and retrieval date.

Run from the repo root:  python scripts/collect_wikipedia.py
Output: data/raw/<year>.wikitext and <year>.meta.json
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

YEARS = [2021, 2022, 2023, 2024]
API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "gaa-match-report-research/0.1 (DkIT MSc dissertation; gsonego@gmail.com)"
OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def fetch_page(title):
    """Return (wikitext, revision metadata) for the current revision of a page."""
    params = {
        "action": "query", "prop": "revisions", "titles": title,
        "rvprop": "ids|timestamp|content", "rvslots": "main",
        "format": "json", "formatversion": "2",
    }
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    rev = data["query"]["pages"][0]["revisions"][0]
    return rev["slots"]["main"]["content"], rev


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for year in YEARS:
        title = f"{year} All-Ireland Senior Football Championship"
        wikitext, rev = fetch_page(title)
        (OUT_DIR / f"{year}.wikitext").write_text(wikitext, encoding="utf-8")
        meta = {
            "title": title,
            "revid": rev["revid"],
            "revision_timestamp": rev["timestamp"],
            "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "permalink": f"https://en.wikipedia.org/w/index.php?oldid={rev['revid']}",
            "licence": "CC BY-SA 4.0",
        }
        (OUT_DIR / f"{year}.meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(f"{year}: revid {rev['revid']}, {len(wikitext):,} chars")


if __name__ == "__main__":
    main()
