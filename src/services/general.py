from wildberries_python_sdk.services.general_sync import SyncGeneralService as WbGeneralService
from src.core.models import User, News, Rating

class GeneralService:
    def __init__(self, client):
        self._service = WbGeneralService(client)

    def get_users(self, is_invite_only: bool = False, limit: int = 100, offset: int = 0) -> list[User]:
        data = self._service.get_users(is_invite_only=is_invite_only, limit=limit, offset=offset)
        users = data.get("users", [])
        return [User(id=u["id"], name=u.get("name", ""), role=u.get("role", "")) for u in users]

    def get_news(self, from_date: str = None, from_id: int = None) -> list[News]:
        data = self._service.get_news(from_date=from_date, from_id=from_id)
        news_items = data.get("news", [])
        return [News(id=n["id"], title=n.get("title", "")) for n in news_items]

    def get_rating(self) -> Rating:
        data = self._service.get_rating()
        return Rating(supplier_id=data.get("supplierId", 0), rating=data.get("rating", 0.0))

    def ping(self) -> dict:
        data = self._service.ping()
        return data