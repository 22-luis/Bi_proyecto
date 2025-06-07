import os
from typing import Any
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.futures import wait
import csv

TABLE_DIR = "../Base Proyecto/"

@task
def scan_directory(path: str) -> list[str]:
    files = [entry.name for entry in os.scandir(path) if entry.is_file() and entry.name in tableFormatting]
    return files

@task
def parse_csv(name: str) -> dict:
    table = {"name": str, "fields": [], "rows": []}
    with open(TABLE_DIR + name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        table["fields"] = next(reader)
        for row in reader:
            table["rows"].append(row)
    table["name"] = name
    return table

def healthcare_datasetFmt(table: dict[str, Any]) -> dict:
    for row in table["rows"]:
        row[1] = row[1].title()
        
    return table

tableFormatting = {
    "healthcare_dataset.csv" : healthcare_datasetFmt
}

@task()
def format_tables(table: dict[str, Any]) -> dict:
    fmtTable = tableFormatting[table["name"]](table)
    if fmtTable is None:
        return Completed(message= "Table format doesn't match")
    return fmtTable
    

@task()
def print_tables(tables: list[dict[str, Any]]) -> None:
    for table in tables:
        print("\n" + table["name"])
        print(*table["fields"], sep=" | ")
        print(*table["rows"][0], sep=" | ")

@flow
def etl() -> None:

    # Extract
    filePaths = scan_directory(TABLE_DIR)
    tables = parse_csv.map(filePaths)
    # print("TABLES:")
    # printTables(tables)
    # Transform
    # Reformat
    fmtTables = format_tables.map(tables)
    wait(fmtTables)
    filtered_tables = [i for i in fmtTables.result() if i is not None]
    print("RESULTS:")
    # print(fmtTables.result())
    print_tables(filtered_tables)
    # Split


if __name__ == "__main__":
    etl()
