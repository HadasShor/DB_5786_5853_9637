from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional

import os

import psycopg2
from psycopg2.extensions import connection as PGConnection
from psycopg2.extras import RealDictCursor


@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    database: str
    user: str
    password: str

    @staticmethod
    def from_env() -> "DbConfig":
        return DbConfig(
            host=os.getenv("PGHOST", "localhost"),
            port=int(os.getenv("PGPORT", "5432")),
            database=os.getenv("PGDATABASE", ""),
            user=os.getenv("PGUSER", ""),
            password=os.getenv("PGPASSWORD", ""),
        )


def connect(cfg: DbConfig) -> PGConnection:
    return psycopg2.connect(
        host=cfg.host,
        port=cfg.port,
        dbname=cfg.database,
        user=cfg.user,
        password=cfg.password,
    )


def fetch_all(conn: PGConnection, sql: str, params: Optional[Iterable[Any]] = None) -> list[dict[str, Any]]:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return list(cur.fetchall())


def execute(conn: PGConnection, sql: str, params: Optional[Iterable[Any]] = None) -> int:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        rowcount = cur.rowcount
    conn.commit()
    return rowcount


def fetch_one(conn: PGConnection, sql: str, params: Optional[Iterable[Any]] = None) -> Optional[dict[str, Any]]:
    rows = fetch_all(conn, sql, params)
    return rows[0] if rows else None

