#!/usr/bin/env python3
"""Lay out bolt-earth-ui-sdk 1.0.0 Maven files under releases/ and remove extras."""
from __future__ import annotations

import shutil
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE = REPO / "releases/io/github/boltearth/bolt-earth-ui-sdk"
VER_DIR = BASE / "1.0.0"

# Upstream currently hosts these under 1.5.0/ with 1.0.1 filenames; bytes match 1.0.0 POM/module.
RAW = (
    "https://raw.githubusercontent.com/adilkhanboltearth/boltearthuisdk/main/"
    "releases/io/github/boltearth/bolt-earth-ui-sdk/1.5.0/"
)


def fetch(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as r:  # noqa: S310
        dest.write_bytes(r.read())


def main() -> None:
    VER_DIR.mkdir(parents=True, exist_ok=True)

    fetch(RAW + "bolt-earth-ui-sdk-1.0.1.pom", VER_DIR / "bolt-earth-ui-sdk-1.0.0.pom")
    fetch(RAW + "bolt-earth-ui-sdk-1.0.1.module", VER_DIR / "bolt-earth-ui-sdk-1.0.0.module")
    fetch(RAW + "bolt-earth-ui-sdk-1.0.1.aar", VER_DIR / "bolt-earth-ui-sdk-1.0.0.aar")

    stamp = time.strftime("%Y%m%d%H%M%S")
    (BASE / "maven-metadata.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <groupId>io.github.boltearth</groupId>
  <artifactId>bolt-earth-ui-sdk</artifactId>
  <versioning>
    <latest>1.0.0</latest>
    <release>1.0.0</release>
    <versions>
      <version>1.0.0</version>
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
        if p.name == "1.0.0" and p.is_dir():
            for child in p.iterdir():
                if child.suffix == ".asc":
                    child.unlink(missing_ok=True)
            continue
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.name == ".DS_Store":
            p.unlink(missing_ok=True)

    idea = REPO / ".idea"
    if idea.is_dir():
        shutil.rmtree(idea, ignore_errors=True)

    for junk in (REPO / ".cursor-write-test.txt",):
        junk.unlink(missing_ok=True)

    names = sorted(x.name for x in VER_DIR.iterdir())
    print("OK", VER_DIR / "bolt-earth-ui-sdk-1.0.0.aar", (VER_DIR / "bolt-earth-ui-sdk-1.0.0.aar").stat().st_size)
    print("artifacts:", names)


if __name__ == "__main__":
    main()
