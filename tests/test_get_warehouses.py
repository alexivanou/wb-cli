import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.cli.main import app

runner = CliRunner()

def test_get_warehouses_command_exists():
    """Проверка, что команда get-warehouses зарегистрирована."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "get-warehouses" in result.output

def test_get_warehouses_no_token():
    """Проверка ошибки при отсутствии токена."""
    result = runner.invoke(app, ["get-warehouses"])
    assert result.exit_code == 1
    assert "API token not provided" in result.output

@patch('src.services.warehouse.WbWarehouseService')
@patch('wildberries_python_sdk.client_sync.SyncClient')
def test_get_warehouses_success(mock_client_cls, mock_service_cls):
    """Проверка успешного выполнения команды с моком."""
    # Настраиваем мок
    mock_service = Mock()
    mock_service.get_warehouses.return_value = [
        {"id": 1, "name": "Warehouse 1", "officeId": 100},
        {"id": 2, "name": "Warehouse 2", "officeId": 200}
    ]
    mock_service_cls.return_value = mock_service
    
    mock_client = Mock()
    mock_client_cls.return_value = mock_client
    
    result = runner.invoke(app, ["get-warehouses", "--token", "test_token"])
    
    assert result.exit_code == 0
    assert "Warehouse" in result.output
    assert "Warehouse 1" in result.output

def test_get_warehouses_json_output():
    """Проверка вывода в формате JSON."""
    with patch('src.services.warehouse.WbWarehouseService') as mock_svc, \
         patch('wildberries_python_sdk.client_sync.SyncClient') as mock_client:
        
        mock_service = Mock()
        mock_service.get_warehouses.return_value = [
            {"id": 1, "name": "Test WH", "officeId": 100}
        ]
        mock_svc.return_value = mock_service
        
        result = runner.invoke(app, ["get-warehouses", "--token", "test_token", "--json"])
        
        assert result.exit_code == 0
        # JSON output should contain the data
        assert "1" in result.output or "Test WH" in result.output