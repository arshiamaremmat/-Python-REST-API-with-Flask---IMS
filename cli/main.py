"""CLI frontend that talks to the Flask API.

Usage examples:
  python -m cli.main list
  python -m cli.main add --name "Soda" --brand "Acme" --price 1.99 --stock 20 --barcode 123
  python -m cli.main get 1
  python -m cli.main update 1 --price 2.49 --stock 15
  python -m cli.main delete 1
  python -m cli.main enrich --barcode 00889497005726
  python -m cli.main enrich --name "almond milk"
"""
from __future__ import annotations
import os
import sys
import argparse
import requests

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")

def _url(path: str) -> str:
    return f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def cmd_list(_: argparse.Namespace) -> int:
    r = requests.get(_url("/inventory"))
    r.raise_for_status()
    for item in r.json():
        print(f"#{item['id']:>3} | {item['name']} ({item['brand']}) | ${item['price']:.2f} | stock={item['stock']}")
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    r = requests.get(_url(f"/inventory/{args.id}"))
    if r.status_code == 404:
        print("Not found")
        return 1
    r.raise_for_status()
    print(r.json())
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    payload = {
        "name": args.name,
        "brand": args.brand,
        "price": args.price,
        "stock": args.stock,
        "barcode": args.barcode,
    }
    r = requests.post(_url("/inventory"), json=payload)
    if r.status_code == 400:
        print("Bad Request:", r.json())
        return 1
    r.raise_for_status()
    print("Created:", r.json())
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    patch = {}
    for field in ("name", "brand", "price", "stock", "barcode"):
        val = getattr(args, field)
        if val is not None:
            patch[field] = val
    r = requests.patch(_url(f"/inventory/{args.id}"), json=patch)
    if r.status_code == 404:
        print("Not found")
        return 1
    r.raise_for_status()
    print("Updated:", r.json())
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    r = requests.delete(_url(f"/inventory/{args.id}"))
    if r.status_code == 404:
        print("Not found")
        return 1
    if r.status_code == 204:
        print("Deleted")
        return 0
    r.raise_for_status()
    return 0


def cmd_enrich(args: argparse.Namespace) -> int:
    if args.barcode:
        r = requests.get(_url(f"/enrich/barcode/{args.barcode}"))
    elif args.name:
        r = requests.get(_url("/enrich/search"), params={"q": args.name})
    else:
        print("Provide --barcode or --name")
        return 1

    if r.status_code == 404:
        print("No product found")
        return 1
    r.raise_for_status()
    print(r.json())
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Inventory Admin Portal CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list", help="List inventory")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("get", help="Get item by id")
    s.add_argument("id", type=int)
    s.set_defaults(func=cmd_get)

    s = sub.add_parser("add", help="Add a new item")
    s.add_argument("--name", required=True)
    s.add_argument("--brand", required=True)
    s.add_argument("--price", required=True, type=float)
    s.add_argument("--stock", required=True, type=int)
    s.add_argument("--barcode")
    s.set_defaults(func=cmd_add)

    s = sub.add_parser("update", help="Update an item (partial)")
    s.add_argument("id", type=int)
    s.add_argument("--name")
    s.add_argument("--brand")
    s.add_argument("--price", type=float)
    s.add_argument("--stock", type=int)
    s.add_argument("--barcode")
    s.set_defaults(func=cmd_update)

    s = sub.add_parser("delete", help="Delete an item by id")
    s.add_argument("id", type=int)
    s.set_defaults(func=cmd_delete)

    s = sub.add_parser("enrich", help="Lookup product via OpenFoodFacts")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--barcode")
    g.add_argument("--name")
    s.set_defaults(func=cmd_enrich)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except requests.RequestException as exc:
        print("Network error:", exc)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

