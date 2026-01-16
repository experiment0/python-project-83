import pytest

from page_analyzer import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    yield client


def test_index_route(client):
    response = client.get("/")
    html = response.data.decode()

    assert response.status_code == 200
    assert '<h1 class="display-3">Анализатор страниц</h1>' in html
    assert \
        '<label for="text" class="visually-hidden">Url для проверки</label>' \
        in html


def test_404(client):
    response = client.get("/not_found_page")
    html = response.data.decode()

    assert response.status_code == 404
    assert "<h1>Страница не найдена</h1>" in html
