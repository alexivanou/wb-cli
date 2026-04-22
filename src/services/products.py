from wildberries_python_sdk.services.products_sync import SyncProductsService as WbProductsService
from src.core.models import Product
from typing import List, Optional

class ProductsService:
    def __init__(self, client):
        self._service = WbProductsService(client)

    def get_products(self, limit: int = 10, offset: int = 0) -> List[Product]:
        # В SDK метод get_cards_list принимает параметры для пагинации
        data = self._service.get_cards_list(
            settings={
                "sort": {
                    "ascending": True
                },
                "cursor": {
                    "limit": limit,
                    "offset": offset
                },
                "filter": {
                    "withPhoto": -1
                }
            }
        )
        # В WB API ответ обычно содержит поле 'cards'
        cards = data.get("cards", [])
        return [Product(**c) for c in cards]
