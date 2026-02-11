from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Rating:
    rate: float
    count: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Rating":
        if data is None:
            return Rating(rate=0.0, count=0)
        return Rating(rate=float(data.get("rate", 0.0)), count=int(data.get("count", 0)))

    def to_dict(self) -> Dict[str, Any]:
        return {"rate": self.rate, "count": self.count}


@dataclass
class Product:
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str
    rating: Optional[Rating] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Product":
        if data is None:
            raise ValueError("Cannot create Product from None")

        rating_data = data.get("rating")
        rating = Rating.from_dict(rating_data) if isinstance(rating_data, dict) else None

        return Product(
            id=int(data.get("id", 0)),
            title=str(data.get("title", "")),
            price=float(data.get("price", 0.0)),
            description=str(data.get("description", "")),
            category=str(data.get("category", "")),
            image=str(data.get("image", "")),
            rating=rating,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "image": self.image,
            "rating": self.rating.to_dict() if self.rating else None,
        }

    @staticmethod
    def list_from_api(data: List[Dict[str, Any]]) -> List["Product"]:
        return [Product.from_dict(item) for item in (data or [])]
