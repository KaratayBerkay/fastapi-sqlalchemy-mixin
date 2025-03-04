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
        is_array: bool = True,
        metadata: Any = None,
    ):
        self._is_list = is_array
        self._query = query
        self._pre_query = pre_query
        self._count: Optional[int] = None
        self.metadata = metadata

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
        return 1

    @property
    def count(self) -> int:
        """Lazy load and return total count of results."""
        if self.is_list and self._count is None:
            self._count = self._query.count()
        elif not self.is_list:
            self._count = 1
        return self._count

    @property
    def query(self) -> Query:
        """Get query object."""
        return self._query

    @property
    def is_list(self) -> bool:
        """Check if response is a list."""
        return self._is_list

    def as_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary format."""
        return {
            "metadata": self.metadata,
            "is_list": self._is_list,
            "query": self.query,
            "count": self.count,
        }
