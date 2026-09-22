import logging
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from db import init_db, query

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("shop")

app = FastAPI(title="Shop API")
init_db()


class CustomerIn(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    city: str | None = None


def row(r):
    return {"id": r[0], "name": r[1], "city": r[2]}


@app.get("/health")
def health():
    query("SELECT 1")  # DB холболт амьд эсэх
    return {"status": "ok"}


@app.get("/version")
def version():
    # Гэрийн даалгавар: APP_ENV-ийг Render Environment дээр production гэж тавина
    return {"version": "1.0", "env": os.environ.get("APP_ENV", "local")}


@app.post("/customers", status_code=201)
def create_customer(p: CustomerIn):
    rows = query(
        "INSERT INTO customers (name, city) VALUES (%s, %s) RETURNING id, name, city",
        (p.name, p.city),
    )
    log.info("customer created id=%s", rows[0][0])
    return row(rows[0])


@app.get("/customers")
def list_customers(city: str | None = None, limit: int = 20):
    sql = "SELECT id, name, city FROM customers"
    if city:
        rows = query(sql + " WHERE city = %s LIMIT %s", (city, limit))
    else:
        rows = query(sql + " LIMIT %s", (limit,))
    return [row(r) for r in rows]


@app.get("/customers/{id}")
def get_customer(id: int):
    rows = query("SELECT id, name, city FROM customers WHERE id = %s", (id,))
    if not rows:
        raise HTTPException(404, "Олдсонгүй")
    return row(rows[0])


@app.patch("/customers/{id}")
def update_customer(id: int, p: CustomerIn):
    rows = query(
        "UPDATE customers SET name = %s, city = %s WHERE id = %s RETURNING id, name, city",
        (p.name, p.city, id),
    )
    if not rows:
        raise HTTPException(404)
    return row(rows[0])


@app.delete("/customers/{id}", status_code=204)
def delete_customer(id: int):
    query("DELETE FROM customers WHERE id = %s", (id,))
