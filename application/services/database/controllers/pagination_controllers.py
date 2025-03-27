from __future__ import annotations
from typing import Any, Dict, Optional, Union
from sqlalchemy import desc, asc
from pydantic import BaseModel

from application.validations.request.list_options.list_options import ListOptions
from application.services.database.controllers.response_controllers import PostgresResponse
from application.api_config import api_configs


class PaginationConfig(BaseModel):
    """
    Configuration for pagination settings.

    Attributes:
        page: Current page number (default: 1)
        size: Items per page (default: 10)
        order_field: Field to order by (default: "id")
        order_type: Order direction (default: "asc")
    """

    page: int = 1
    size: int = 10
    order_field: Optional[Union[tuple[str], list[str]]] = None
    order_type: Optional[Union[tuple[str], list[str]]] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.order_field is None:
            self.order_field = ["uu_id"]
        if self.order_type is None:
            self.order_type = ["asc"]


class Pagination:
    """
    Handles pagination logic for query results.

    Manages page size, current page, ordering, and calculates total pages
    and items based on the data source.

    Attributes:
        DEFAULT_SIZE: Default number of items per page
        MIN_SIZE: Minimum allowed page size
        MAX_SIZE: Maximum allowed page size
    """

    DEFAULT_SIZE: int = int(api_configs.DEFAULT_SIZE or 10)
    MIN_SIZE: int = int(api_configs.MIN_SIZE or 5)
    MAX_SIZE: int = int(api_configs.MAX_SIZE or 50)

    def __init__(self, data: PostgresResponse):
        self._data = data
        self.size: int = self.DEFAULT_SIZE
        self.page: int = 1
        self.orderField: Optional[Union[tuple[str], list[str]]] = ["uu_id"]
        self.orderType: Optional[Union[tuple[str], list[str]]] = ["asc"]
        self.page_count: int = 1
        self.total_count: int = 0
        self.all_count: int = 0
        self.total_pages: int = 1
        self._update_page_counts()

    @property
    def data(self) -> Union[list, dict]:
        return self._data.data

    def change(self, **kwargs) -> None:
        """Update pagination settings from config."""
        config = PaginationConfig(**kwargs)
        self.size = (
            config.size
            if self.MIN_SIZE <= config.size <= self.MAX_SIZE
            else self.DEFAULT_SIZE
        )
        self.page = config.page
        self.orderField = config.order_field
        self.orderType = config.order_type
        self._update_page_counts()

    def feed(self, data: PostgresResponse) -> None:
        """Calculate pagination based on data source."""
        self._data = data
        self._update_page_counts()

    def _update_page_counts(self) -> None:
        """Update page counts and validate current page."""
        if self.data:
            self.total_count = self._data.count
            self.all_count = self._data.total_count

        self.size = (
            self.size
            if self.MIN_SIZE <= self.size <= self.MAX_SIZE
            else self.DEFAULT_SIZE
        )
        self.total_pages = max(1, (self.total_count + self.size - 1) // self.size)
        self.page = max(1, min(self.page, self.total_pages))
        self.page_count = (
            self.total_count % self.size
            if self.page == self.total_pages and self.total_count % self.size
            else self.size
        )

    def refresh(self) -> None:
        """Reset pagination state to defaults."""
        self._update_page_counts()

    def reset(self) -> None:
        """Reset pagination state to defaults."""
        self.size = self.DEFAULT_SIZE
        self.page = 1
        self.orderField = "uu_id"
        self.orderType = "asc"

    def as_dict(self) -> Dict[str, Any]:
        """Convert pagination state to dictionary format."""
        self.refresh()
        return {
            "size": self.size,
            "page": self.page,
            "allCount": self.all_count,
            "totalCount": self.total_count,
            "totalPages": self.total_pages,
            "pageCount": self.page_count,
            "orderField": self.orderField,
            "orderType": self.orderType,
        }


class PaginationResult:
    """
    Result of a paginated query.

    Contains the query result and pagination state.
    data: PostgresResponse of query results
    pagination: Pagination state

    Attributes:
        _query: Original query object
        pagination: Pagination state
    """

    def __init__(
        self, data: PostgresResponse, pagination: Pagination, response_model: Any = None
    ):
        self._data = data
        self._query = data.query
        self._core_query = data.core_query
        self.pagination = pagination
        self.response_type = data.is_list
        self.limit = self.pagination.size
        self.offset = self.pagination.size * (self.pagination.page - 1)
        self.order_by = self.pagination.orderField
        self.order_type = self.pagination.orderType
        self.response_model = response_model

    def dynamic_order_by(self):
        """
        Dynamically order a query by multiple fields.
        Returns:
            Ordered query object.
        """
        if not len(self.order_by) == len(self.order_type):
            raise ValueError(
                "Order by fields and order types must have the same length."
            )
        order_criteria = zip(self.order_by, self.order_type)
        print('order_criteria', order_criteria)
        if not self._data.data:
            return self._core_query

        for field, direction in order_criteria:
            print('field', field, direction)
            columns = self._data.data[0].filterable_attributes
            print('columns', columns)
            if field in columns:
                if direction.lower().startswith("d"):
                    self._core_query = self._core_query.order_by(
                        desc(
                            getattr(self._core_query.column_descriptions[0]["entity"], field)
                        )
                    )
                else:
                    self._core_query = self._core_query.order_by(
                        asc(
                            getattr(self._core_query.column_descriptions[0]["entity"], field)
                        )
                    )
        return self._core_query

    @property
    def data(self) -> Union[list | dict]:
        """Get query object."""
        query_ordered = self.dynamic_order_by()
        query_paginated = query_ordered.limit(self.limit).offset(self.offset)
        queried_data = (
            query_paginated.all() if self.response_type else query_paginated.first()
        )
        data = (
            [result.get_dict() for result in queried_data]
            if self.response_type
            else queried_data.get_dict()
        )
        if self.response_model:
            return [self.response_model(**item).model_dump() for item in data]
        return data


class QueryOptions:

    def __init__(
        self,
        table,
        data: Union[dict, ListOptions] = None,
        model_query: Optional[Any] = None,
    ):
        self.table = table
        self.data = data
        self.model_query = model_query
        if isinstance(data, dict):
            self.data = ListOptions(**data)
        self.validate_query()
        if not self.data.order_type:
            self.data.order_type = ["created_at"]
        if not self.data.order_field:
            self.data.order_field = ["uu_id"]

    def validate_query(self):
        if not self.data.query or not self.model_query:
            return ()
        cleaned_query, cleaned_query_by_model, last_dict = {}, {}, {}
        for key, value in self.data.query.items():
            cleaned_query[str(str(key).split("__")[0])] = value
            cleaned_query_by_model[str(str(key).split("__")[0])] = (key, value)
        cleaned_model = self.model_query(**cleaned_query)
        for i in cleaned_query:
            if hasattr(cleaned_model, i):
                last_dict[str(cleaned_query_by_model[str(i)][0])] = str(
                    cleaned_query_by_model[str(i)][1]
                )
        self.data.query = last_dict

    def convert(self) -> tuple:
        """
        self.table.convert(query)
        (<sqlalchemy.sql.elements.BinaryExpression object at 0x7caaeacf0080>, <sqlalchemy.sql.elements.BinaryExpression object at 0x7caaea729b80>)
        """
        if not self.data or self.data.query:
            return ()
        return tuple(self.table.convert(self.data.query))
