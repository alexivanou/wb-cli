from wildberries_python_sdk.services.inventory_sync import SyncInventoryService as WbInventoryService
from src.core.models import InventoryItem
from typing import List, Any

class InventoryService:
    def __init__(self, client):
        self._service = WbInventoryService(client)

    def get_inventory(self, warehouse_id: int, chrt_ids: List[int]) -> List[InventoryItem]:
        # Метод SDK возвращает словарь с данными. Посмотрим, как выглядит структура.
        # Обычно это {'stocks': [...]} или список словарей.
        data = self._service.get_inventory(warehouse_id=warehouse_id, chrt_ids=chrt_ids)
        
        # Исходя из структуры SDK, data - это часто dict, нужно правильно распарсить
        stocks = data.get("stocks", [])
        return [InventoryItem(**item) for item in stocks]
