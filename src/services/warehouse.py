from wildberries_python_sdk.services.warehouse_sync import SyncWarehouseService as WbWarehouseService
from src.core.models import Warehouse
from typing import List

class WarehouseService:
    def __init__(self, client):
        self._service = WbWarehouseService(client)

    def get_warehouses(self) -> List[Warehouse]:
        data = self._service.get_warehouses()
        # Маппинг данных (учитывая, что WB SDK возвращает dict, Pydantic распарсит)
        return [Warehouse(**w) for w in data]
