from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Database connection
def dbconnect():
    return sqlite3.connect('simple_shop.db')

# Function to create the database and tables if they don't exist
def initialize_database():
    connection = sqlite3.connect('simple_shop.db')
    cursor = connection.cursor()

    # Create products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    );
    """)

    # Create customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """)

    # Create orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );
    """)

    # Create order_items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    """)

    cursor.close()
    connection.close()

@app.on_event("startup")
async def startup_event():
    initialize_database()

# Pydantic models for data validation
class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

class NewProduct(BaseModel):
    name: str
    price: float
    quantity: int

class Customer(BaseModel):
    id: int
    name: str
    email: str

class NewCustomer(BaseModel):
    name: str
    email: str

class Order(BaseModel):
    id: int
    customer_id: int
    order_date: str
    status: str

class NewOrder(BaseModel):
    customer_id: int
    status: str

class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float

class NewOrderItem(BaseModel):
    order_id: int
    product_id: int
    quantity: int

@app.post("/products/", response_model=Product)
async def create_product(product: NewProduct):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?);",
                   (product.name, product.price, product.quantity))
    connection.commit()
    cursor.execute("SELECT id FROM products WHERE name = ?;", (product.name,))
    product_id = cursor.fetchone()[0]  # Fetching the id directly (sqlite3 returns a tuple)
    cursor.close()
    connection.close()
    return Product(id=product_id, name=product.name, price=product.price, quantity=product.quantity)

@app.get("/products/", response_model=List[Product])
async def get_all_products():
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products;")
    products = cursor.fetchall()  # Returns a list of tuples
    cursor.close()
    connection.close()
    return [Product(id=p[0], name=p[1], price=p[2], quantity=p[3]) for p in products]  # Accessing by index

@app.get("/products/{product_id}", response_model=Product)
async def get_product_by_id(product_id: int):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?;", (product_id,))
    product = cursor.fetchone()  # Returns a tuple
    cursor.close()
    connection.close()
    if product:
        return Product(id=product[0], name=product[1], price=product[2], quantity=product[3])
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: NewProduct):
    connection = dbconnect() 
    cursor = connection.cursor()
    cursor.execute("""UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?;""", 
                   (product.name, product.price, product.quantity, product_id))
    connection.commit()
    cursor.execute("SELECT * FROM products WHERE id = ?;", (product_id,))
    updated_product = cursor.fetchone()  # Returns a tuple
    cursor.close()
    connection.close()
    if updated_product:
        return Product(id=updated_product[0], name=updated_product[1], 
                       price=updated_product[2], quantity=updated_product[3])
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?;", (product_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Product deleted"}






##############################################################################################################
# 6. Create Customer
# @app.post("/customers/", response_model=Customer)
# async def create_customer(customer: NewCustomer):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s);",
#                    (customer.name, customer.email))
#     connection.commit()
#     cursor.execute("SELECT id FROM customers WHERE email = %s;", (customer.email,))
#     customer_id = cursor.fetchone()['id']
#     cursor.close()
#     connection.close()
#     return Customer(id=customer_id, name=customer.name, email=customer.email)

# # 7. Get All Customers
# @app.get("/customers/", response_model=List[Customer])
# async def get_all_customers():
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM customers;")
#     customers = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return [Customer(id=c['id'], name=c['name'], email=c['email']) for c in customers]

# # 8. Get Customer by ID
# @app.get("/customers/{customer_id}", response_model=Customer)
# async def get_customer_by_id(customer_id: int):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM customers WHERE id = %s;", (customer_id,))
#     customer = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     if customer:
#         return Customer(id=customer['id'], name=customer['name'], email=customer['email'])
#     raise HTTPException(status_code=404, detail="Customer not found")

# # 9. Update Customer
# @app.put("/customers/{customer_id}", response_model=Customer)
# async def update_customer(customer_id: int, customer: NewCustomer):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("""
#         UPDATE customers SET name = %s, email = %s WHERE id = %s;
#     """, (customer.name, customer.email, customer_id))
#     connection.commit()
#     cursor.execute("SELECT * FROM customers WHERE id = %s;", (customer_id,))
#     updated_customer = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     if updated_customer:
#         return Customer(id=updated_customer['id'], name=updated_customer['name'],
#                         email=updated_customer['email'])
#     raise HTTPException(status_code=404, detail="Customer not found")

# # 10. Delete Customer by ID
# @app.delete("/customers/{customer_id}")
# async def delete_customer(customer_id: int):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("DELETE FROM customers WHERE id = %s;", (customer_id,))
#     connection.commit()
#     cursor.close()
#     connection.close()
#     return {"message": "Customer deleted"}

# # 11. Create Order
# @app.post("/orders/", response_model=Order)
# async def create_order(order: NewOrder):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO orders (customer_id, order_date, status) VALUES (%s, NOW(), %s);",
#                    (order.customer_id, order.status))
#     connection.commit()
#     cursor.execute("SELECT id FROM orders WHERE customer_id = %s AND status = %s ORDER BY order_date DESC LIMIT 1;",
#                    (order.customer_id, order.status))
#     order_id = cursor.fetchone()['id']
#     cursor.close()
#     connection.close()
#     return Order(id=order_id, customer_id=order.customer_id, order_date='', status=order.status)

# # 12. Get All Orders
# @app.get("/orders/", response_model=List[Order])
# async def get_all_orders():
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM orders;")
#     orders = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return [Order(id=o['id'], customer_id=o['customer_id'],
#                   order_date=o['order_date'].strftime('%Y-%m-%d %H:%M:%S'),
#                   status=o['status']) for o in orders]

# # 13. Get Order by ID
# @app.get("/orders/{order_id}", response_model=Order)
# async def get_order_by_id(order_id: int):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM orders WHERE id = %s;", (order_id,))
#     order = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     if order:
#         return Order(id=order['id'], customer_id=order['customer_id'],
#                      order_date=order['order_date'].strftime('%Y-%m-%d %H:%M:%S'), status=order['status'])
#     raise HTTPException(status_code=404, detail="Order not found")

# # 14. Update Order
# @app.put("/orders/{order_id}", response_model=Order)
# async def update_order(order_id: int, order: NewOrder):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("""
#         UPDATE orders SET customer_id = %s, status = %s WHERE id = %s;
#     """, (order.customer_id, order.status, order_id))
#     connection.commit()
#     cursor.execute("SELECT * FROM orders WHERE id = %s;", (order_id,))
#     updated_order = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     if updated_order:
#         return Order(id=updated_order['id'], customer_id=updated_order['customer_id'],
#                      order_date=updated_order['order_date'].strftime('%Y-%m-%d %H:%M:%S'), status=updated_order['status'])
#     raise HTTPException(status_code=404, detail="Order not found")

# # 15. Delete Order by ID
# @app.delete("/orders/{order_id}")
# async def delete_order(order_id: int):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("DELETE FROM orders WHERE id = %s;", (order_id,))
#     connection.commit()
#     cursor.close()
#     connection.close()
#     return {"message": "Order deleted"}
# # 16. Create Order Item
# @app.post("/order-items/", response_model=OrderItem)
# async def create_order_item(order_item: NewOrderItem):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("""
#         INSERT INTO order_items (order_id, product_id, quantity, price)
#         SELECT %s, %s, %s, price FROM products WHERE id = %s;
#     """, (order_item.order_id, order_item.product_id, order_item.quantity, order_item.product_id))
#     connection.commit()
#     cursor.execute("SELECT id FROM order_items WHERE order_id = %s AND product_id = %s;",
#                    (order_item.order_id, order_item.product_id))
#     order_item_id = cursor.fetchone()['id']
#     cursor.close()
#     connection.close()
#     return OrderItem(id=order_item_id, order_id=order_item.order_id, product_id=order_item.product_id,
#                      quantity=order_item.quantity, price=order_item.price)

# # 17. Get All Order Items
# @app.get("/order-items/", response_model=List[OrderItem])
# async def get_all_order_items():
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM order_items;")
#     order_items = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return [OrderItem(id=o['id'], order_id=o['order_id'], product_id=o['product_id'],
#                       quantity=o['quantity'], price=o['price']) for o in order_items]

# # 18. Get Order Items by Order ID
# @app.get("/order-items/order/{order_id}", response_model=List[OrderItem])
# async def get_order_items_by_order_id(order_id: int):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM order_items WHERE order_id = %s;", (order_id,))
#     order_items = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return [OrderItem(id=o['id'], order_id=o['order_id'], product_id=o['product_id'],
#                       quantity=o['quantity'], price=o['price']) for o in order_items]

# # 19. Get Order Items by Product ID
# @app.get("/order-items/product/{product_id}", response_model=List[OrderItem])
# async def get_order_items_by_product_id(product_id: int):
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM order_items WHERE product_id = %s;", (product_id,))
#     order_items = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return [OrderItem(id=o['id'], order_id=o['order_id'], product_id=o['product_id'],
#                       quantity=o['quantity'], price=o['price']) for o in order_items]

# # 20. Get Total Sales
# @app.get("/sales/total")
# async def get_total_sales():
#     connection = dbconnect()
#     cursor = connection.cursor()
#     cursor.execute("""
#     SELECT SUM(quantity * price) AS total_sales FROM order_items;
#     """)
#     total_sales = cursor.fetchone()['total_sales']
#     cursor.close()
#     connection.close()
#     return {"total_sales": total_sales}


