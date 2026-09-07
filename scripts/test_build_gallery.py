import json
import pathlib


def test_manifest_exists():
    assert pathlib.Path("site/src/data/gallery.json").exists()


def test_thumbs_generated():
    assert list(pathlib.Path("site/public/thumbs/fullhd").glob("*.webp"))


def test_count_134():
    data = json.loads(pathlib.Path("site/src/data/gallery.json").read_text())
    assert len(data) == 134
    cats = {x["category"] for x in data}
    assert cats == {"fullhd", "classic", "special", "phone", "art"}
