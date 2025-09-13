from unittest.mock import patch
from app import external


def test_fetch_by_barcode_success():
    fake = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "code": "00889497005726",
            "ingredients_text": "Filtered water, almonds, cane sugar",
            "nutriscore_grade": "b",
            "image_front_url": "https://example.com/img.jpg",
        },
    }
    with patch("app.external.requests.get") as mget:
        mget.return_value.json.return_value = fake
        mget.return_value.raise_for_status.return_value = None
        out = external.fetch_by_barcode("00889497005726")
    assert out["name"] == "Organic Almond Milk"
    assert out["brand"] == "Silk"


def test_search_by_name_no_results():
    fake = {"products": []}
    with patch("app.external.requests.get") as mget:
        mget.return_value.json.return_value = fake
        mget.return_value.raise_for_status.return_value = None
        out = external.search_by_name("nonexistent brand")
    assert out is None