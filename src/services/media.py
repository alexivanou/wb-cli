from wildberries_python_sdk.services.media_sync import SyncMediaService as WbMediaService
from src.core.models import MediaItem
from typing import List

class MediaService:
    def __init__(self, client):
        self._service = WbMediaService(client)

    def get_media(self, nm_id: int) -> MediaItem:
        data = self._service.get_media(nm_id=nm_id)
        return MediaItem(**data)
