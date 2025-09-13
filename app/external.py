"""OpenFoodFacts client wrapper.

This module centralizes HTTP calls so we can mock them easily in tests.
"""
from __future__ import annotations
from typing import Any, Dict, Optional
import os
import requests

OFF_PRODUCT_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
OFF_SEARCH_URL = (
    "https://world.openfoodfacts.org/cgi/search.pl"
)

DEFAULT_TIMEOUT = float(os.getenv("OFF_TIMEOUT", 6.0))


def fetch_by_barcode(barcode: str) -> Optional[Dict[str, Any]]:
    url = OFF_PRODUCT_URL.format(barcode=barcode)
    r = requests.get(url, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if data.get("status") == 1:
        product = data.get("product", {})
        return _shape_product(product)
    return None


def search_by_name(name: str) -> Optional[Dict[str, Any]]:
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }
    r = requests.get(OFF_SEARCH_URL, params=params, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    payload = r.json() or {}
    products = payload.get("products", [])
    if not products:
        return None
    return _shape_product(products[0])


def _shape_product(p: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize OpenFoodFacts fields into our internal shape."""
    return {
        "name": p.get("product_name"),
        "brand": p.get("brands"),
        "barcode": p.get("code") or p.get("_id"),
        "ingredients": p.get("ingredients_text"),
        # Optional extras for future use
        "nutriscore_grade": p.get("nutriscore_grade"),
        "image_url": p.get("image_front_url") or p.get("image_url"),
    }