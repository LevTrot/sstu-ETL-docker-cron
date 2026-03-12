import psycopg2
from faker import Faker
import random

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    database="shop",
    user="admin",
    password="admin"
)

cur = conn.cursor()

customers = []
orders = []
products = []

print("Spam customers")

for i in range(10000):

    cur.execute(
        "INSERT INTO customers(name,email) VALUES(%s,%s) RETURNING id",
        (fake.name(), fake.email())
    )

    customers.append(cur.fetchone()[0])

conn.commit()

product_names = ["Laptop","Mouse","Keyboard","Monitor","Headphones","Samsung(dangerous)"]

print("Spam products")

for i in range(10000):

    cur.execute(
        "INSERT INTO products(name,price) VALUES(%s,%s) RETURNING id",
        (
            random.choice(product_names),
            random.randint(10,2000)
        )
    )

    products.append(cur.fetchone()[0])

conn.commit()

print("Spam orders")

for i in range(500000):

    cur.execute(
        """
        INSERT INTO orders(customer_id,product,amount)
        VALUES(%s,%s,%s)
        RETURNING id
        """,
        (
            random.choice(customers),
            fake.word(),
            round(random.uniform(10,1000),2)
        )
    )

    orders.append(cur.fetchone()[0])

    if i % 10000 == 0:
        conn.commit()
        print("Inserted orders:", i)

conn.commit()

print("Spam order_products")

for order_id in orders:

    for _ in range(random.randint(1,3)):

        cur.execute(
            """
            INSERT INTO order_products(order_id,product_id,quantity)
            VALUES(%s,%s,%s)
            """,
            (
                order_id,
                random.choice(products),
                random.randint(1,5)
            )
        )

conn.commit()

cur.close()
conn.close()

print("Done.")