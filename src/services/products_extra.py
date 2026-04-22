from wildberries_python_sdk.services.products_sync import SyncProductsService as WbProductsService
from typing import List, Any

class ProductsServiceExtra:
    def __init__(self, client):
        self._service = WbProductsService(client)

    def get_brands(self) -> List[dict]:
        return self._service.get_brands()

    def get_subjects(self) -> List[dict]:
        return self._service.get_subjects()

    def get_tags(self) -> List[dict]:
        return self._service.get_tags()

    def get_parent_categories(self) -> List[dict]:
        return self._service.get_parent_categories()

    def get_colors(self) -> List[dict]:
        return self._service.get_colors()

    def get_countries(self) -> List[dict]:
        return self._service.get_countries()

    def get_seasons(self) -> List[dict]:
        return self._service.get_seasons()

    def get_genders(self) -> List[dict]:
        return self._service.get_genders()