import strawberry
from typing import List

@strawberry.type
class OrderItem:
    name: str
    price: float

@strawberry.type
class Order:
    id: int
    status: str
    items: List[OrderItem]

@strawberry.type
class Query:
    @strawberry.field
    def order(self, id: int) -> Order:
        return Order(
            id=id, 
            status="SHIPPED", 
            items=[OrderItem(name="Laptop", price=1200.0)]
        )

schema = strawberry.Schema(query=Query)
