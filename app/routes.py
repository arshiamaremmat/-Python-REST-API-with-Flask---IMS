from flask import Blueprint, jsonify, request, abort
from . import inventory
from . import external

bp = Blueprint("api", __name__)

# ---- Inventory CRUD ----
@bp.get("/inventory")
def api_list():
    return jsonify(inventory.list_items()), 200


@bp.get("/inventory/<int:item_id>")
def api_get(item_id: int):
    item = inventory.get_item(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item), 200


@bp.post("/inventory")
def api_post():
    data = request.get_json(silent=True) or {}
    required = ["name", "brand", "price", "stock"]
    if any(k not in data for k in required):
        return jsonify({"error": "Missing required fields: name, brand, price, stock"}), 400
    item = inventory.add_item(data)
    return jsonify(item), 201


@bp.patch("/inventory/<int:item_id>")
def api_patch(item_id: int):
    data = request.get_json(silent=True) or {}
    updated = inventory.update_item(item_id, data)
    if not updated:
        return jsonify({"error": "Not found"}), 404
    return jsonify(updated), 200


@bp.delete("/inventory/<int:item_id>")
def api_delete(item_id: int):
    ok = inventory.delete_item(item_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    # 204 No Content to signal success without payload
    return ("", 204)


# ---- External API enrichment ----
@bp.get("/enrich/barcode/<barcode>")
def enrich_barcode(barcode: str):
    data = external.fetch_by_barcode(barcode)
    if not data:
        return jsonify({"error": "No product found for barcode"}), 404
    return jsonify(data), 200


@bp.get("/enrich/search")
def enrich_search():
    q = request.args.get("q", type=str)
    if not q:
        return jsonify({"error": "Missing query param 'q'"}), 400
    data = external.search_by_name(q)
    if not data:
        return jsonify({"error": "No product found for query"}), 404
    return jsonify(data), 200