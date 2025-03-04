from typing import Optional
from pydantic import BaseModel


class ListOptions(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 10
    order_field: Optional[list[str]] = None
    order_type: Optional[list[str]] = None
    query: Optional[dict] = None
