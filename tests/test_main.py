import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["DATABASE_URL"] = "sqlite:///./test_app.db"

from app.main import app  # noqa: E402

# Usado como context manager para o evento de startup (criação de tabelas) rodar.
client = TestClient(app)
client.__enter__()


def test_versao():
    response = client.get("/versao")
    assert response.status_code == 200
    assert response.json() == {"versao": "1.0"}


def test_root_redirects_to_docs():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (301, 302, 307)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_list_items_empty():
    response = client.get("/items/")
    assert response.status_code == 200
