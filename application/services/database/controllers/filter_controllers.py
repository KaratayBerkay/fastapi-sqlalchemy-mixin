"""
Advanced filtering functionality for SQLAlchemy models.

This module provides a comprehensive set of filtering capabilities for SQLAlchemy models,
including pagination, ordering, and complex query building.
"""

from __future__ import annotations
from typing import Any, TypeVar, Type, Union, Optional

from sqlalchemy import ColumnExpressionArgument
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.elements import BinaryExpression

from services.database.controllers.response_controllers import PostgresResponse


T = TypeVar("T", bound="QueryModel")


class QueryModel:

    pre_query = None
    __abstract__ = True

    @classmethod
    def _query(cls: Type[T], db: Session) -> Query:
        """Returns the query to use in the model."""
        return cls.pre_query if cls.pre_query else db.query(cls)

    @classmethod
    def produce_query_to_add(cls: Type[T], filter_list):
        if filter_list.get("query"):
            for smart_iter in cls.filter_expr(**filter_list["query"]):
                if key := getattr(getattr(smart_iter, "left", None), "key", None):
                    args = cls.add_new_arg_to_args(args, key, smart_iter)

    @classmethod
    def convert(
        cls: Type[T], smart_options: dict, validate_model: Any = None
    ) -> Optional[tuple[BinaryExpression]]:
        if not validate_model:
            return tuple(cls.filter_expr(**smart_options))

    @classmethod
    def filter_by_one(
        cls: Type[T], db: Session, system: bool = False, **kwargs
    ) -> PostgresResponse:
        """
        Filter single record by keyword arguments.

        Args:
            db: Database session
            system: If True, skip status filtering
            **kwargs: Filter criteria

        Returns:
            Query response with single record
        """
        if "is_confirmed" not in kwargs and not system:
            kwargs["is_confirmed"] = True
        kwargs.pop("system", None)
        query = cls._query(db).filter_by(**kwargs)
        return PostgresResponse(pre_query=cls._query(db), query=query, is_array=False)

    @classmethod
    def filter_one(
        cls: Type[T],
        *args: Union[BinaryExpression, ColumnExpressionArgument],
        db: Session,
    ) -> PostgresResponse:
        """
        Filter single record by expressions.

        Args:
            db: Database session
            args: Filter expressions

        Returns:
            Query response with single record
        """
        args = cls.get_not_expired_query_arg(args)
        query = cls._query(db=db).filter(*args)
        return PostgresResponse(
            pre_query=cls._query(db=db), query=query, is_array=False
        )

    @classmethod
    def filter_one_system(
        cls,
        *args: Union[BinaryExpression, ColumnExpressionArgument],
        db: Session,
    ):
        query = cls._query(db=db).filter(*args)
        return PostgresResponse(
            pre_query=cls._query(db=db), query=query, is_array=False
        )

    @classmethod
    def filter_all_system(
        cls: Type[T],
        *args: Union[BinaryExpression, ColumnExpressionArgument],
        db: Session,
    ) -> PostgresResponse:
        """
        Filter multiple records by expressions without status filtering.

        Args:
            db: Database session
            args: Filter expressions

        Returns:
            Query response with matching records
        """

        query = cls._query(db)
        query = query.filter(*args)
        return PostgresResponse(pre_query=cls._query(db), query=query, is_array=True)

    @classmethod
    def filter_all(
        cls: Type[T],
        *args: Union[BinaryExpression, ColumnExpressionArgument],
        db: Session,
    ) -> PostgresResponse:
        """
        Filter multiple records by expressions.

        Args:
            db: Database session
            args: Filter expressions
        Returns:
            Query response with matching records
        """
        args = cls.get_not_expired_query_arg(args)
        query = cls._query(db).filter(*args)
        return PostgresResponse(pre_query=cls._query(db), query=query, is_array=True)

    @classmethod
    def filter_by_all_system(cls: Type[T], db: Session, **kwargs) -> PostgresResponse:
        """
        Filter multiple records by keyword arguments.

        Args:
            db: Database session
            **kwargs: Filter criteria

        Returns:
            Query response with matching records
        """
        query = cls._query(db).filter_by(**kwargs)
        return PostgresResponse(pre_query=cls._query(db), query=query, is_array=True)
