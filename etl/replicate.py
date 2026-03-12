import psycopg2
import os
from pymongo import MongoClient

pg = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

mongo = MongoClient(f"mongodb://{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}")

mdb = mongo["shop"]
collection = mdb["customers"]

cur = pg.cursor()

cur.execute("""
SELECT
    c.id,
    c.name,
    c.email,
    c.deleted_at,
    o.id,
    o.deleted_at,
    p.name,
    p.price,
    p.deleted_at,
    op.quantity
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
LEFT JOIN order_products op ON op.order_id = o.id
LEFT JOIN products p ON p.id = op.product_id
""")

rows = cur.fetchall()

customers = {}

for r in rows:

    cid, name, email, c_deleted, order_id, o_deleted, product, price, p_deleted, quantity = r

    if cid not in customers:
        customers[cid] = {
            "_id": cid,
            "name": name,
            "email": email,
            "deleted_at": c_deleted,
            "orders": {}
        }

    orders = customers[cid]["orders"]

    if order_id not in orders:
        orders[order_id] = {
            "order_id": order_id,
            "deleted_at": o_deleted,
            "products": []
        }

    orders[order_id]["products"].append({
        "name": product,
        "price": float(price) if price is not None else 0.0,
        "quantity": quantity,
        "deleted_at": p_deleted
    })

for customer in customers.values():
    customer["orders"] = list(customer["orders"].values())

for doc in customers.values():
    collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)

print("Replication complete")