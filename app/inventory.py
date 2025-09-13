from itertools import count
from typing import Any, Dict, List, Optional

_items: List[Dict[str, Any]] = []
_id_counter = count(1)

if not _items:
    _items.extend([
        {
            "id": next(_id_counter),
            "name": "Organic Almond Milk",
            "brand": "Silk",
            "barcode": "00889497005726",
            "price": 3.99,
            "stock": 12,
            "ingredients": "Filtered water, almonds, cane sugar",
        },
        {
            "id": next(_id_counter),
            "name": "Dark Chocolate Bar 70%",
            "brand": "Green & Black's",
            "barcode": "0741082412312",
            "price": 2.49,
            "stock": 30,
            "ingredients": "Cocoa mass, sugar, cocoa butter, vanilla",
        },
    ])


def list_items() -> List[Dict[str, Any]]:
    return list(_items)


def get_item(item_id: int) -> Optional[Dict[str, Any]]:
    return next((i for i in _items if i["id"] == item_id), None)


def add_item(data: Dict[str, Any]) -> Dict[str, Any]:
    item = {
        "id": next(_id_counter),
        "name": data.get("name"),
        "brand": data.get("brand"),
        "barcode": data.get("barcode"),
        "price": float(data.get("price", 0)),
        "stock": int(data.get("stock", 0)),
        "ingredients": data.get("ingredients"),
    }
    _items.append(item)
    return item


def update_item(item_id: int, partial: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    item = get_item(item_id)
    if not item:
        return None
    # Only update known fields
    for key in ["name", "brand", "barcode", "price", "stock", "ingredients"]:
        if key in partial:
            if key == "price" and partial[key] is not None:
                item[key] = float(partial[key])
            elif key == "stock" and partial[key] is not None:
                item[key] = int(partial[key])
            else:
                item[key] = partial[key]
    return item


def delete_item(item_id: int) -> bool:
    idx = next((i for i, itm in enumerate(_items) if itm["id"] == item_id), None)
    if idx is None:
        return False
    _items.pop(idx)
    return True