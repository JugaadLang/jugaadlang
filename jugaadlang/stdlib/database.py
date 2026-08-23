"""
JugaadORM — SQLite-backed Object-Relational Mapper for JugaadLang.
"""

from __future__ import annotations
import sqlite3
import contextlib
from typing import Any, Optional, Type, TypeVar

T = TypeVar("T", bound="Model")


class Field:
    """Base Field type."""

    def __init__(self, sql_type: str, primary_key: bool = False, default: Any = None) -> None:
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.default = default


class String(Field):
    """Text column."""

    def __init__(self, default: Optional[str] = None) -> None:
        super().__init__("TEXT", default=default)


class Integer(Field):
    """Integer column."""

    def __init__(self, primary_key: bool = False, default: Optional[int] = None) -> None:
        super().__init__("INTEGER", primary_key=primary_key, default=default)


class Float(Field):
    """Float/Real column."""

    def __init__(self, default: Optional[float] = None) -> None:
        super().__init__("REAL", default=default)


class Boolean(Field):
    """Boolean column mapped to integer (0 or 1)."""

    def __init__(self, default: Optional[bool] = None) -> None:
        val = None if default is None else (1 if default else 0)
        super().__init__("INTEGER", default=val)


class Model:
    """
    Base class for JugaadORM models.
    """

    id: Any = Integer(primary_key=True)
    _db_path: str = "jugaad.db"

    def __init__(self, **kwargs: Any) -> None:
        self._fields: dict[str, Field] = {}
        for base in reversed(self.__class__.__mro__):
            for name, attr in base.__dict__.items():
                if isinstance(attr, Field):
                    self._fields[name] = attr
                    # Set default
                    setattr(self, name, kwargs.get(name, attr.default))

        # Ensure id is initialized
        if "id" not in kwargs:
            self.id = None

    @classmethod
    def connect(cls) -> sqlite3.Connection:
        """Get connection to SQLite database."""
        conn = sqlite3.connect(cls._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def table_name(cls) -> str:
        """Get table name derived from class name."""
        return cls.__name__.lower()

    @classmethod
    def banao_table(cls) -> None:
        """Create SQLite table if it doesn't exist."""
        fields = {}
        for base in reversed(cls.__mro__):
            for name, attr in base.__dict__.items():
                if isinstance(attr, Field):
                    fields[name] = attr

        fields_sql = []
        for name, attr in fields.items():
            sql = f"{name} {attr.sql_type}"
            if attr.primary_key:
                sql += " PRIMARY KEY AUTOINCREMENT"
            fields_sql.append(sql)

        sql_stmt = f"CREATE TABLE IF NOT EXISTS {cls.table_name()} ({', '.join(fields_sql)});"
        with contextlib.closing(cls.connect()) as conn:
            with conn:
                try:
                    conn.execute(sql_stmt)
                    conn.commit()
                except Exception:
                    conn.rollback()
                    raise

    @classmethod
    def drop_table(cls) -> None:
        """Drop SQLite table if it exists."""
        with contextlib.closing(cls.connect()) as conn:
            with conn:
                try:
                    sql_stmt = f"DROP TABLE IF EXISTS {cls.table_name()};"
                    conn.execute(sql_stmt)
                    conn.commit()
                except Exception:
                    conn.rollback()
                    raise

    def bachao(self) -> None:
        """Save (insert or update) record to database."""
        # Ensure table exists
        self.banao_table()

        field_names = [name for name in self._fields.keys() if name != "id"]

        with contextlib.closing(self.connect()) as conn:
            with conn:
                try:
                    cursor = conn.cursor()
                    if self.id is None:
                        # Insert
                        placeholders = ", ".join(["?"] * len(field_names))
                        values = [getattr(self, name) for name in field_names]
                        sql = f"INSERT INTO {self.table_name()} ({', '.join(field_names)}) VALUES ({placeholders})"
                        cursor.execute(sql, values)
                        self.id = cursor.lastrowid
                    else:
                        # Update
                        set_clause = ", ".join([f"{name} = ?" for name in field_names])
                        values = [getattr(self, name) for name in field_names] + [self.id]
                        sql = f"UPDATE {self.table_name()} SET {set_clause} WHERE id = ?"
                        cursor.execute(sql, values)
                    conn.commit()
                except Exception:
                    conn.rollback()
                    raise

    def mitao(self) -> None:
        """Delete record from database."""
        if self.id is None:
            return
        with contextlib.closing(self.connect()) as conn:
            with conn:
                try:
                    sql = f"DELETE FROM {self.table_name()} WHERE id = ?"
                    conn.execute(sql, (self.id,))
                    conn.commit()
                except Exception:
                    conn.rollback()
                    raise
            self.id = None

    @classmethod
    def sab(cls: Type[T]) -> list[T]:
        """Fetch all records."""
        cls.banao_table()
        with contextlib.closing(cls.connect()) as conn:
            with conn:
                cursor = conn.execute(f"SELECT * FROM {cls.table_name()}")
                rows = cursor.fetchall()

                results = []
                for row in rows:
                    obj = cls(**dict(row))
                    obj.id = row["id"]
                    results.append(obj)
                return results

    @classmethod
    def filter(cls: Type[T], **kwargs: Any) -> list[T]:
        """Filter records by key-value parameters."""
        cls.banao_table()
        if not kwargs:
            return cls.sab()

        where_clause = " AND ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values())

        with contextlib.closing(cls.connect()) as conn:
            with conn:
                cursor = conn.execute(f"SELECT * FROM {cls.table_name()} WHERE {where_clause}", values)
                rows = cursor.fetchall()

                results = []
                for row in rows:
                    obj = cls(**dict(row))
                    obj.id = row["id"]
                    results.append(obj)
                return results
