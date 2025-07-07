from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        price REAL,
        stock INTEGER
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TEXT,
        status TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        hire_date TEXT,
        salary REAL,
        department_id INTEGER,
        FOREIGN KEY(department_id) REFERENCES departments(department_id)
    );''')
    conn.commit()
    conn.close()

def populate_db_from_sql(file_path):
    if not os.path.exists(file_path):
        print(f"SQL file {file_path} not found.")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    conn = get_db_connection()
    conn.executescript(sql_script)
    conn.commit()
    conn.close()
    print("Database populated from SQL script.")

def mysql_dump_to_sqlite(input_file: str, output_file: str):
    """
    Converts a MySQL dump SQL file to a SQLite-compatible SQL file,
    disabling foreign keys during import and re-enabling them at the end.
    """
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    output_lines = [
        "-- Converted by mysql_dump_to_sqlite\n",
        "PRAGMA foreign_keys = OFF;\n\n"  # 🚩 Disattiva vincoli all'inizio
    ]

    skip_prefixes = [
        "--", "/*!", "USE ", "DROP DATABASE", "CREATE DATABASE", "LOCK TABLES", "UNLOCK TABLES", "SET "
    ]

    for line in lines:
        stripped = line.strip()

        if any(stripped.startswith(prefix) for prefix in skip_prefixes) or stripped == "":
            continue

        # Rimozioni generiche
        for pattern in [
            "ENGINE=InnoDB", "DEFAULT CHARSET=utf8mb4", "CHARSET=utf8mb4",
            "COLLATE utf8mb4_0900_ai_ci", "/*!80016 DEFAULT ENCRYPTION='N' */",
            "AUTO_INCREMENT"
        ]:
            line = line.replace(pattern, "")

        if "CONSTRAINT" in line and "FOREIGN KEY" in line:
            parts = line.split("FOREIGN KEY")
            line = "FOREIGN KEY" + parts[1]

        if " KEY " in line:
            continue

        line = line.replace(" int ", " INTEGER ")
        line = line.replace(" int,", " INTEGER,")
        line = line.replace(" int(", " INTEGER(")
        line = line.replace(" double ", " REAL ")
        line = line.replace(" double,", " REAL,")
        line = line.replace(" datetime ", " TEXT ")
        line = line.replace(" datetime,", " TEXT,")
        line = line.replace(" date ", " TEXT ")
        line = line.replace(" date,", " TEXT,")
        line = line.replace("`", "")

        if line.strip() == ");":
            if output_lines[-1].strip().endswith(","):
                output_lines[-1] = output_lines[-1].rstrip(",\n") + "\n"

        output_lines.append(line)

    # 🚩 Riattiva vincoli alla fine
    output_lines.append("\nPRAGMA foreign_keys = ON;\n")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(output_lines)

    print(f"[✔] Converted with PRAGMA foreign_keys toggling, saved to {output_file}")

# init_db()
mysql_dump_to_sqlite('db_a.sql', 'db_b.sql')
populate_db_from_sql('db_b.sql')

class CreateOrderRequest(BaseModel):
    customer_id: int
    items: List[dict]

class UpdateOrderStatusRequest(BaseModel):
    order_id: int
    new_status: str

@app.post("/create-order")
def create_order(request: CreateOrderRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_id, order_date, status) VALUES (?, DATE('now'), ?)",
                   (request.customer_id, "in lavorazione"))
    order_id = cursor.lastrowid
    for item in request.items:
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                       (order_id, item['product_id'], item['quantity']))
    conn.commit()
    conn.close()
    return {"message": "Order created successfully", "order_id": order_id}

@app.put("/update-order-status")
def update_order_status(request: UpdateOrderStatusRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (request.new_status, request.order_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order status updated successfully"}

@app.get("/order/{order_id}")
def get_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {**dict(order), "items": items}

@app.get("/customer/{customer_id}")
def get_customer(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(customer)

@app.get("/product/{product_id}")
def get_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(product)

@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return dict(employee)

@app.get("/department/{department_id}")
def get_department(department_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM departments WHERE department_id = ?", (department_id,))
    department = cursor.fetchone()
    conn.close()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return dict(department)

# To run: uvicorn orders_api_fastapi:app --reload

# if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="127.0.0.1", port=8000)