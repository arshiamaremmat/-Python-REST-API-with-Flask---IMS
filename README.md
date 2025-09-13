# -Python-REST-API-with-Flask---Inventory Management System

An end-to-end lab project providing:

- **Flask REST API** with CRUD routes for `/inventory`
- **External API integration** with OpenFoodFacts (barcode search + name search)
- **CLI frontend** to interact with the API (list, get, add, update, delete, enrich)
- **Unit tests** with `pytest` and `unittest.mock`


## Quick Start

### 1) Environment
```bash
python -V               # 3.10+
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
````