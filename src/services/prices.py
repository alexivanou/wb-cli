from wildberries_python_sdk.services.prices_sync import SyncPricesService as WbPricesService
from src.core.models import PriceUpdate

class PricesService:
    def __init__(self, client):
        self._service = WbPricesService(client)

    def set_prices_and_discounts(self, nm_id: int, price: int, discount: int) -> None:
        payload = [{"nmId": nm_id, "price": price, "discount": discount}]
        self._service.set_prices_and_discounts(data=payload)
