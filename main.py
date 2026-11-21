"""news-image-20261121 entry: the world on Saturday 21 November 2026.

entry.png is the finished 1024x1024 front page (39 stories, 13 illustrated
cards with a place banner each, a map of where it happened and 26 numbered
briefs). The sandbox runs
this file with no network; it checks the picture, then writes the very same
bytes on every run.
"""
import pathlib
import sys
from os import environ

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SIZE_CAP = 1024 * 1024  # the bounty accepts at most 1 MiB


def load_page() -> bytes:
    page = pathlib.Path(__file__).with_name("entry.png").read_bytes()
    if not page.startswith(PNG_MAGIC):
        sys.exit("entry.png is not a PNG file")
    if len(page) > SIZE_CAP:
        sys.exit(f"entry.png is {len(page)} bytes, over the 1 MiB cap")
    width = int.from_bytes(page[16:20], "big")  # IHDR: width, then height
    height = int.from_bytes(page[20:24], "big")
    if width > 1024 or height > 1024:
        sys.exit(f"entry.png is {width}x{height}, larger than 1024x1024")
    return page


def deliver() -> None:
    out_dir = pathlib.Path(environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(load_page())
    print(f"saved {target} ({target.stat().st_size} bytes)")


deliver()
