import sqlite3

from main import main, Product

# ... (Previous code for classes and functions)

# Connect to SQLite database
conn = sqlite3.connect("marketplace.db")
cursor = conn.cursor()

# Create a table for products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        username  TEXT  PRIMARY KEY,
        password TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userid INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')


# Commit the changes and close the connection
conn.commit()
conn.close()


class AdminFunctions:
    def __init__(self):
        pass

    def add_product_to_database(self, product):
        # Connect to SQLite database
        conn = sqlite3.connect("marketplace.db")
        cursor = conn.cursor()

        # Insert product into the products table
        cursor.execute('''
                INSERT INTO products (name, category, price)
                VALUES (?, ?, ?)
            ''', (product.name, product.category, product.price))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    def extract_product_from_database(self, product_id):
        # Connect to SQLite database
        conn = sqlite3.connect("marketplace.db")
        cursor = conn.cursor()

        # Retrieve product information from the database
        cursor.execute('''
            SELECT * FROM products WHERE product_id = ?
        ''', (product_id,))
        result = cursor.fetchone()

        # Close the connection
        conn.close()

        if result:
            product_id, name, category, price = result
            return Product(product_id, name, category, price)
        else:
            return None

    def delete_product_from_database(self, product_id):
        # Connect to SQLite database
        conn = sqlite3.connect("marketplace.db")
        cursor = conn.cursor()

        # Delete product from the products table
        cursor.execute('''
            DELETE FROM products WHERE product_id = ?
        ''', (product_id,))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    def check_admin_auth(self,username,passwd):
        conn = sqlite3.connect("marketplace.db")
        cursor = conn.cursor()

        # Retrieve admin  information from the database
        cursor.execute('''
                   SELECT * FROM admin WHERE username = ? and password = ?
               ''', [username,passwd])
        result = cursor.fetchone()

        # Close the connection
        conn.close()

        if result:
            username,passwd = result
            return 'Pass'
        else:
            return 'Fail'

# ... (The rest of the previous code)


if __name__ == "__main__":
    main()
