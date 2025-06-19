import os
from prefect import task
import csv

@task
def scan_directory(path: str, tables: list[str]) -> list[str]:
    files = [entry.path for entry in os.scandir(path) if entry.is_file() and entry.name in tables]
    return files

@task
def parse_csv(path: str) -> dict:
    table = {"name": str, "fields": [], "rows": []}
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        table["fields"] = next(reader)
        for row in reader:
            table["rows"].append(row)
    table["name"] = csv_file.name.split("/")[-1]
    return table