"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

# Travel Agency app schemas

class Offer(BaseModel):
    """
    Travel offers collection schema
    Collection name: "offer"
    """
    title: str = Field(..., description="Offer title (e.g., Bali Getaway 5D4N)")
    description: Optional[str] = Field(None, description="Short description of the offer")
    price: float = Field(..., ge=0, description="Price in USD")
    destination: str = Field(..., description="Destination city/country")
    image_url: Optional[HttpUrl] = Field(None, description="Hero image URL for the offer")
    is_featured: bool = Field(False, description="Highlight this offer on the homepage")

class Post(BaseModel):
    """
    Agency posts/announcements
    Collection name: "post"
    """
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content or announcement body")
    image_url: Optional[HttpUrl] = Field(None, description="Optional image to accompany the post")

class Review(BaseModel):
    """
    Customer reviews
    Collection name: "review"
    """
    name: str = Field(..., description="Customer name")
    rating: int = Field(..., ge=1, le=5, description="Star rating from 1-5")
    comment: Optional[str] = Field(None, description="Review comment")
    trip: Optional[str] = Field(None, description="What trip this review refers to")

# Example schemas (kept for reference; not used by this app)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
