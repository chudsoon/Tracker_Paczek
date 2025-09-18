import pytest
from unittest.mock import MagicMock

from widgets.admin_panel import AdminPanel  # Zmień ścieżkę jeśli inna
from textual.widgets import Static, Button


@pytest.mark.asyncio
async def test_load_user_list_success(monkeypatch):
    """Testuje poprawne załadowanie listy użytkownoyików."""
    mock_users = [{"full_name": "Jan Kowalski"}, {"full_name": "Anna Nowak"}]

    def mock_get(url):
        mock_response = MagicMock()
        mock_response.json.return_value = mock_users
        return mock_response

    monkeypatch.setattr("widgets.admin_panel.httpx.get", mock_get)

    panel = AdminPanel()
    await panel.mount()
    panel.load_user_list()

    buttons = list(panel.query(Button).results())
    labels = [btn.label for btn in buttons]

    assert "Jan Kowalski" in labels
    assert "Anna Nowak" in labels


@pytest.mark.asyncio
async def test_load_user_list_empty(monkeypatch):
    """Testuje sytuację gdy lista użytkowników jest pusta."""

    def mock_get(url):
        mock_response = MagicMock()
        mock_response.json.return_value = []
        return mock_response

    monkeypatch.setattr("widgets.admin_panel.httpx.get", mock_get)

    panel = AdminPanel()
    await panel.mount()
    panel.load_user_list()

    static_texts = [s.renderable for s in panel.query(Static).results()]
    assert any("Brak uzytkowników" in text for text in static_texts)


@pytest.mark.asyncio
async def test_load_user_list_error(monkeypatch):
    """Testuje sytuację gdy zapytanie rzuca wyjątek."""

    def mock_get(url):
        raise Exception("Błąd połączenia")

    monkeypatch.setattr("widgets.admin_panel.httpx.get", mock_get)

    panel = AdminPanel()
    await panel.mount()
    panel.load_user_list()

    static_texts = [s.renderable for s in panel.query(Static).results()]
    assert any("Błąd" in text for text in static_texts)
