import sqlite3


class Product:
    def __init__(self, product_id, name, category, price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.categories = ["Footwear", "Clothing", "Electronics"]

        # Connect to SQLite database for products
        self.conn_products = sqlite3.connect("marketplace.db")
        self.cursor_products = self.conn_products.cursor()

        # Create a table for products
        self.cursor_products.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        price REAL NOT NULL
                    )
                ''')

        # Commit the changes
        self.conn_products.commit()

    def display_product_from_database(self):
        self.cursor_products.execute('''
            SELECT * FROM products
        ''')
        print('getting all data')
        result = self.cursor_products.fetchall()
        print(result)
        if not result:
            print("No products found.")
        else:
            print("All Products:")
            for product in result:
                product_id, name, category, price = product
                print(f"{product_id}. {name} ({category}): ${price}")


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity=1):
        self.items.append({"product": product, "quantity": quantity})

    def remove_item(self, product_id):
        self.items = [item for item in self.items if item["product"].product_id != product_id]

    def view_cart(self):
        for item in self.items:
            product = item["product"]
            quantity = item["quantity"]
            print(f"{product.name} ({product.category}): ${product.price} x {quantity}")


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def admin_login(username, password):
    return username == "admin" and password == "adminpass"


class AdminFunctions:
    def __init__(self):
        self.products = Product(None, None, None, None)
        self.categories = ["Footwear", "Clothing", "Electronics"]

        # Connect to SQLite database for products
        self.conn_products = sqlite3.connect("marketplace.db")
        self.cursor_products = self.conn_products.cursor()

        # Create a table for products
        self.cursor_products.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')

        # Commit the changes
        self.conn_products.commit()

        # Connect to SQLite database for users
        self.conn_users = sqlite3.connect("marketplace.db")
        self.cursor_users = self.conn_users.cursor()

        # Create a table for users
        self.cursor_users.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Commit the changes
        self.conn_users.commit()

    def add_product_to_database(self, product):
        # Insert product into the products table
        self.cursor_products.execute('''
            INSERT INTO products (name, category, price)
            VALUES (?, ?, ?)
        ''', (product.name, product.category, product.price))

        # Commit the changes
        self.conn_products.commit()

    def extract_product_from_database(self, product_id):
        # Retrieve product information from the products table
        self.cursor_products.execute('''
            SELECT * FROM products WHERE product_id = ?
        ''', (product_id,))
        result = self.cursor_products.fetchone()

        if result:
            product_id, name, category, price = result
            return Product(product_id, name, category, price)
        else:
            return None

    def modify_product_in_database(self, product_id, new_price):
        # Modify product price in the products table
        self.cursor_products.execute('''
            UPDATE products SET price = ? WHERE product_id = ?
        ''', (new_price, product_id))

        # Commit the changes
        self.conn_products.commit()

    def remove_product_from_database(self, product_id):
        # Delete product from the products table
        self.cursor_products.execute('''
            DELETE FROM products WHERE product_id = ?
        ''', (product_id,))

        # Commit the changes
        self.conn_products.commit()

    def add_category(self, category):
        self.categories.append(category)
        print(f"{category} category added.")

    def remove_category(self, category):
        if category in self.categories:
            self.categories.remove(category)
            print(f"{category} category removed.")
        else:
            print("Category not found.")

    def add_user_to_database(self, username, password):
        # Insert user into the users table
        self.cursor_users.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
            ''', (username, password))

        # Commit the changes
        self.conn_users.commit()

    def remove_user_from_database(self, username):
        # Delete user from the users table
        self.cursor_users.execute('''
            DELETE FROM users WHERE username = ?
        ''', (username,))

        # Commit the changes
        self.conn_users.commit()

    def display_all_products(self):
        self.products.display_product_from_database()
    def __del__(self):
        # Close the database connections
        self.conn_products.close()
        self.conn_users.close()


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserFunctions:
    def __init__(self):
        self.cart = ShoppingCart()

        # Connect to SQLite database for users
        self.conn = sqlite3.connect("marketplace.db")
        self.cursor = self.conn.cursor()

        # Create a table for users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Commit the changes
        self.conn.commit()

    def user_login(self, username, password):
        return self.verify_user_credentials(username, password)

    def add_user_to_database(self, username, password):
        # Insert user into the users table
        self.cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, password))

        # Commit the changes
        self.conn.commit()

    def remove_user_from_database(self, username):
        # Delete user from the users table
        self.cursor.execute('''
            DELETE FROM users WHERE username = ?
        ''', (username,))

        # Commit the changes
        self.conn.commit()

    def verify_user_credentials(self, username, password):
        # Verify user credentials against the users table
        self.cursor.execute('''
            SELECT * FROM users WHERE username = ? AND password = ?
        ''', (username, password))
        result = self.cursor.fetchone()

        if result:
            return True
        else:
            return False

    def __del__(self):
        # Close the database connection
        self.conn.close()


def main():
    print("Welcome to the Demo Marketplace")

    user_functions = UserFunctions()
    admin_functions = AdminFunctions()

    while True:
        print("\n1. User Login")
        print("2. Admin Login")
        print("3. Register User")
        print("4. Exit")

        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            user_username = input("Enter user username: ")
            user_password = input("Enter user password: ")

            if user_functions.user_login(user_username, user_password):
                print("User login successful.")
                while True:
                    print("\nUser Functions:")
                    print("1. View Product")
                    print("2. Add to Cart")
                    print("3. Remove from Cart")
                    print("4. View Cart")
                    print("5. Checkout")
                    print("6. Logout")

                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        admin_functions.display_all_products()
                    elif user_choice == "2":
                        admin_functions.display_all_products()
                        product_id = int(input("Enter the product ID to add to cart: "))
                        quantity = int(input("Enter the quantity: "))
                        product = admin_functions.extract_product_from_database(product_id)
                        if product:
                            user_functions.cart.add_item(product, quantity)
                            print(f"{product.name} added to your cart.")
                        else:
                            print("Invalid product ID.")
                    elif user_choice == "3":
                        product_id = int(input("Enter the product ID to remove from cart: "))
                        user_functions.cart.remove_item(product_id)
                    elif user_choice == "4":
                        user_functions.cart.view_cart()
                    elif user_choice == "5":
                        total_price = sum(
                            item["product"].price * item["quantity"]
                            for item in user_functions.cart.items
                        )
                        print(f"Total Price: ${total_price}")
                        print("Your order is successfully placed.")
                        break
                    elif user_choice == "6":
                        print("User logout.")
                        break
                    else:
                        print("Invalid choice. Please select a valid option.")

            else:
                print("User login failed. Incorrect username or password.")

        elif user_choice == "2":
            admin_username = input("Enter admin username: ")
            admin_password = input("Enter admin password: ")

            if admin_login(admin_username, admin_password):
                print("Admin login successful.")
                while True:
                    print("\nAdmin Functions:")
                    print("1. Add Product")
                    print("2. Modify Product Price")
                    print("3. Remove Product")
                    print("4. Add Category")
                    print("5. Remove Category")
                    print("6. Add User")
                    print("7. Remove User")
                    print("8. Logout")

                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":
                        product_id = int(input("Enter product ID: "))
                        name = input("Enter product name: ")
                        category = input("Enter product category: ")
                        price = float(input("Enter product price: "))
                        new_product = Product(product_id, name, category, price)

                        # Add the product to the database
                        admin_functions.add_product_to_database(new_product)

                        print(f"{new_product.name} added to the product catalog.")
                    elif admin_choice == "2":
                        product_id = int(input("Enter product ID to modify: "))
                        new_price = float(input("Enter the new price: "))

                        # Modify the product in the database
                        admin_functions.modify_product_in_database(product_id, new_price)

                        print(f"Product with ID {product_id} price updated.")
                    elif admin_choice == "3":
                        product_id = int(input("Enter product ID to remove: "))

                        # Delete the product from the database
                        admin_functions.remove_product_from_database(product_id)

                        print(f"Product with ID {product_id} removed from the catalog.")
                    elif admin_choice == "4":
                        new_category = input("Enter new category: ")
                        admin_functions.add_category(new_category)
                    elif admin_choice == "5":
                        category_to_remove = input("Enter category to remove: ")
                        admin_functions.remove_category(category_to_remove)
                    elif admin_choice == "6":
                        new_user_username = input("Enter new username: ")
                        new_user_password = input("Enter new password: ")

                        # Add the user to the database
                        admin_functions.add_user_to_database(new_user_username, new_user_password)

                        print(f"User {new_user_username} added.")
                    elif admin_choice == "7":
                        username_to_remove = input("Enter username to remove: ")

                        # Remove the user from the database
                        admin_functions.remove_user_from_database(username_to_remove)

                        print(f"User {username_to_remove} removed.")
                    elif admin_choice == "8":
                        print("Admin logout.")
                        break
                    else:
                        print("Invalid choice. Please select a valid option.")

            else:
                print("Admin login failed. Incorrect username or password.")

        elif user_choice == "3":
            new_user_username = input("Enter new username: ")
            new_user_password = input("Enter new password: ")

            # Add the user to the database
            user_functions.add_user_to_database(new_user_username, new_user_password)
            print(f"User {new_user_username} registered successfully.")

        elif user_choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
