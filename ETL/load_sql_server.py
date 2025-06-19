import os
from typing import Any
from prefect import task, flow
from prefect.cache_policies import NO_CACHE
import pyodbc

DB_NAME = 'DW'

CONN_STR = f'Driver={{ODBC Driver 17 for SQL Server}};Server=.\\TESTDW;Database={DB_NAME};Trusted_Connection=yes;'

@task
def connect() -> pyodbc.Connection:
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


def test_read(conn):
    print("Read")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT TABLE_NAME FROM {DB_NAME}.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    allrows = cursor.fetchall()
    for row in allrows:
        print(f'row = {row}')
        print()


test_read(pyodbc.connect(CONN_STR))

