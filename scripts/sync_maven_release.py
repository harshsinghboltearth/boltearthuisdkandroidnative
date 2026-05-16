#!/usr/bin/env python3
"""Download base artifacts from GitHub and lay out bolt-earth-ui-sdk at VERSION under releases/."""
from __future__ import annotations

import json
import shutil
import time
import urllib.request
from pathlib import Path

# Published coordinate version (change here when you ship a new drop).
VERSION = "1.0.6"

REPO = Path(__file__).resolve().parent.parent
BASE = REPO / "releases/io/github/boltearth/bolt-earth-ui-sdk"
VER_DIR = BASE / VERSION

# Raw files on main (may use older filenames; content is rewritten for VERSION).
RAW = (
    "https://raw.githubusercontent.com/adilkhanboltearth/boltearthuisdk/main/"
    "releases/io/github/boltearth/bolt-earth-ui-sdk/1.0.0/"
)


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url) as r:  # noqa: S310
        return r.read()


def main() -> None:
    VER_DIR.mkdir(parents=True, exist_ok=True)

    aar = fetch(RAW + "bolt-earth-ui-sdk-1.0.0.aar")
    pom_raw = fetch(RAW + "bolt-earth-ui-sdk-1.0.0.pom").decode("utf-8")
    mod_data = json.loads(fetch(RAW + "bolt-earth-ui-sdk-1.0.0.module").decode("utf-8"))

    marker_old = "<artifactId>bolt-earth-ui-sdk</artifactId>\n  <version>1.0.0</version>"
    marker_new = f"<artifactId>bolt-earth-ui-sdk</artifactId>\n  <version>{VERSION}</version>"
    if marker_old not in pom_raw:
        raise SystemExit("Unexpected POM: project version marker missing")
    pom_raw = pom_raw.replace(marker_old, marker_new, 1)

    mod_data["component"]["version"] = VERSION
    for variant in mod_data["variants"]:
        for f in variant.get("files", []):
            if f.get("name", "").endswith(".aar"):
                f["name"] = f"bolt-earth-ui-sdk-{VERSION}.aar"
                f["url"] = f"bolt-earth-ui-sdk-{VERSION}.aar"

    (VER_DIR / f"bolt-earth-ui-sdk-{VERSION}.aar").write_bytes(aar)
    (VER_DIR / f"bolt-earth-ui-sdk-{VERSION}.pom").write_text(pom_raw, encoding="utf-8")
    (VER_DIR / f"bolt-earth-ui-sdk-{VERSION}.module").write_text(
        json.dumps(mod_data, indent=2) + "\n", encoding="utf-8"
    )

    stamp = time.strftime("%Y%m%d%H%M%S")
    (BASE / "maven-metadata.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <groupId>io.github.boltearth</groupId>
  <artifactId>bolt-earth-ui-sdk</artifactId>
  <versioning>
    <latest>{VERSION}</latest>
    <release>{VERSION}</release>
    <versions>
      <version>{VERSION}</version>
    </versions>
    <lastUpdated>{stamp}</lastUpdated>
  </versioning>
</metadata>
""",
        encoding="utf-8",
    )

    if not BASE.is_dir():
        return

    for p in BASE.iterdir():
        if p.name == "maven-metadata.xml":
            continue
        if p.name == VERSION and p.is_dir():
            for child in p.iterdir():
                if child.suffix == ".asc":
                    child.unlink(missing_ok=True)
            continue
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.name == ".DS_Store":
            p.unlink(missing_ok=True)

    print("OK", VER_DIR / f"bolt-earth-ui-sdk-{VERSION}.aar")


if __name__ == "__main__":
    main()
