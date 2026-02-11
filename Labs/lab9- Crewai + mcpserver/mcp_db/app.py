import sqlite3
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI(title="MCP Database Proxy")

DB_PATH = "./data.db"


def get_conn():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn


def init_db():
	conn = get_conn()
	cur = conn.cursor()
	cur.execute(
		"""
		CREATE TABLE IF NOT EXISTS items (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			external_id TEXT,
			source TEXT,
			title TEXT,
			body TEXT,
			extra TEXT
		)
		"""
	)
	conn.commit()
	conn.close()


class InsertItem(BaseModel):
	external_id: str
	source: str
	title: str
	body: str = ""
	extra: dict = {}


@app.on_event("startup")
def on_startup():
	init_db()


@app.post("/insert/items")
def insert_items(items: List[InsertItem]):
	"""Insert a list of normalized items into the SQLite database.

	All database access must go through this MCP server.
	"""
	conn = get_conn()
	cur = conn.cursor()
	inserted = 0
	for it in items:
		cur.execute(
			"INSERT INTO items (external_id, source, title, body, extra) VALUES (?, ?, ?, ?, ?)",
			(it.external_id, it.source, it.title, it.body, json.dumps(it.extra)),
		)
		inserted += 1
	conn.commit()
	conn.close()
	return {"inserted": inserted}


@app.get("/items")
def list_items():
	conn = get_conn()
	cur = conn.cursor()
	cur.execute("SELECT id, external_id, source, title, body, extra FROM items ORDER BY id ASC")
	rows = cur.fetchall()
	result = []
	for r in rows:
		result.append(
			{
				"id": r["id"],
				"external_id": r["external_id"],
				"source": r["source"],
				"title": r["title"],
				"body": r["body"],
				"extra": json.loads(r["extra"] or "{}"),
			}
		)
	conn.close()
	return result