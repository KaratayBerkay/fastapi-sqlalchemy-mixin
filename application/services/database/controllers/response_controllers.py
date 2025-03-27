"""
Response handler for PostgreSQL query results.

This module provides a wrapper class for SQLAlchemy query results,
adding convenience methods for accessing data and managing query state.
"""

from typing import Any, Dict, Optional, TypeVar, Generic, Union
from sqlalchemy.orm import Query


T = TypeVar("T")


class PostgresResponse(Generic[T]):
    """
    Wrapper for PostgreSQL/SQLAlchemy query results.

    Attributes:
        metadata: Additional metadata for the query

    Properties:
        count: Total count of results
        query: Get query object
        as_dict: Convert response to dictionary format
    """

    def __init__(
        self,
        pre_query: Query,
        query: Query,
        model,
        is_array: bool = True,
        metadata: Any = None,
    ):
        self._core_class = model
        self._is_list = is_array
        self._query = query
        self._pre_query = pre_query
        self._count: Optional[int] = None
        self.metadata = metadata

    @property
    def core_class(self):
        """Get query object."""
        return self._core_class

    @property
    def data(self) -> Union[T, list[T]]:
        """Get query results."""
        if not self.is_list:
            first_item = self._query.first()
            return first_item if first_item else None
        return self._query.all() if self._query.all() else []

    @property
    def data_as_dict(self) -> Union[Dict[str, Any], list[Dict[str, Any]]]:
        """Get query results as dictionary."""
        if self.is_list:
            first_item = self._query.first()
            return first_item.get_dict() if first_item.first() else None
        all_items = self._query.all()
        return [result.get_dict() for result in all_items] if all_items else []

    @property
    def total_count(self) -> int:
        """Lazy load and return total count of results."""
        if self.is_list:
            return self._pre_query.count() if self._pre_query else 0
        if self.data:
            return 1
        return 0

    @property
    def count(self) -> int:
        """Lazy load and return total count of results."""
        if self.data and not isinstance(self.data, list):
            return 1
        elif self.data and isinstance(self.data, list):
            return len(self.data)
        return 0

    @property
    def query(self) -> str:
        """Get query object."""
        return str(self._query)

    @property
    def core_query(self) -> Query:
        """Get query object."""
        return self._query

    @property
    def is_list(self) -> bool:
        """Check if response is a list."""
        return self._is_list

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary format."""
        if isinstance(self.data, list):
            return {
                "metadata": self.metadata,
                "is_list": self._is_list,
                "query": str(self.query),
                "count": self.count,
                "data": [result.get_dict() for result in self.data],
            }
        return {
            "metadata": self.metadata,
            "is_list": self._is_list,
            "query": str(self.query),
            "count": self.count,
            "data": self.data.get_dict() if self.data else {},
        }
