from unittest.mock import patch
from cli import main as cli_main


def test_cli_list(monkeypatch, capsys):
    # Mock requests.get for /inventory
    class R:
        status_code = 200
        def json(self):
            return [
                {"id": 1, "name": "A", "brand": "B", "price": 1.0, "stock": 2},
                {"id": 2, "name": "C", "brand": "D", "price": 2.5, "stock": 5},
            ]
        def raise_for_status(self):
            return None

    with patch("cli.main.requests.get", return_value=R()):
        rc = cli_main.main(["list"])  # type: ignore
        assert rc == 0
        out = capsys.readouterr().out
        assert "#  1" in out and "#  2" in out


def test_cli_add(monkeypatch, capsys):
    class R:
        status_code = 201
        def json(self):
            return {"id": 99, "name": "Soda"}
        def raise_for_status(self):
            return None

    with patch("cli.main.requests.post", return_value=R()):
        rc = cli_main.main([
            "add", "--name", "Soda", "--brand", "Acme", "--price", "1.99", "--stock", "10"
        ])  # type: ignore
        assert rc == 0
        assert "Created:" in capsys.readouterr().out