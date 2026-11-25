"""Lectura de datos de prueba desde archivos externos (CSV / JSON)."""
import csv
import json

from utils.config import DATA_DIR


def read_csv(filename: str) -> list[dict]:
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_json(filename: str):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)
