import os
from typing import Any
from prefect import task, flow
from prefect.cache_policies import NO_CACHE
import pyodbc



@task
def connect(CONN_STR) -> pyodbc.Connection:
    conn = pyodbc.connect(CONN_STR)
    return conn

@task(cache_policy=NO_CACHE)
def clear(conn: pyodbc.Connection, tableData: dict[str, Any]):
    cursor = conn.cursor()
    cursor.execute(f"delete from {tableData["name"]};")
    try:
        cursor.execute(f"DBCC CHECKIDENT ({tableData["name"]}, RESEED, 0);")
    except Exception:
        pass
    conn.commit()

@task(cache_policy=NO_CACHE)
def load(conn: pyodbc.Connection, tableData: dict[str, Any]):
    cursor = conn.cursor()
    sql = f"insert into {tableData["name"]} ({", ".join(tableData["fields"])}) values ({("?, "*len(tableData["fields"]))[:-2]});"
    cursor.executemany(sql, tableData["rows"])
    conn.commit()