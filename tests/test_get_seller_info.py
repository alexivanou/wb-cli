import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.cli.main import app

runner = CliRunner()

def test_get_seller_info_command_exists():
    """Проверка, что команда get-seller-info зарегистрирована."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "get-seller-info" in result.output

def test_get_seller_info_no_token():
    """Проверка ошибки при отсутствии токена."""
    result = runner.invoke(app, ["get-seller-info"])
    assert result.exit_code == 1
    assert "API token not provided" in result.output