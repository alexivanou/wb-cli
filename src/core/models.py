from pydantic import BaseModel, Field
from typing import Optional, List

class SellerInfo(BaseModel):
    """Business model for Seller Information."""
    name: str
    supplier_id: str = Field(alias="sid")

class Warehouse(BaseModel):
    """Business model for Warehouse."""
    id: int = Field(alias="id")
    name: str
    office_id: int = Field(alias="officeId")

class InventoryItem(BaseModel):
    """Business model for Inventory Item."""
    chrt_id: int = Field(alias="chrtId")
    amount: int

class Product(BaseModel):
    """Business model for Product."""
    nm_id: int = Field(alias="nmID")
    vendor_code: str = Field(alias="vendorCode")
    subject_name: str = Field(alias="subjectName")

class MediaItem(BaseModel):
    """Business model for Media Item."""
    nm_id: int = Field(alias="nmID")
    photo_links: List[str] = Field(alias="photoLinks")

class PriceUpdate(BaseModel):
    """Business model for Price Update."""
    nm_id: int = Field(alias="nmID")
    price: int
    discount: int

class User(BaseModel):
    """Business model for User."""
    id: int
    name: str
    role: str

class News(BaseModel):
    """Business model for News."""
    id: int
    title: str

class Rating(BaseModel):
    """Business model for Rating."""
    supplier_id: int
    rating: float
