import kivy
import requests  # Add this import for making HTTP requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

kivy.require('2.1.0')

# FastAPI server URL
API_BASE_URL = "http://localhost:8000/products/"

# Home Screen
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        
        product_button = Button(text="Manage Products")
        product_button.bind(on_press=self.navigate_to_products)

        customer_button = Button(text="Manage Customers")
        customer_button.bind(on_press=self.navigate_to_customers)

        order_button = Button(text="Manage Orders")
        order_button.bind(on_press=self.navigate_to_orders)

        layout.add_widget(product_button)
        layout.add_widget(customer_button)
        layout.add_widget(order_button)
        
        self.add_widget(layout)

    def navigate_to_products(self, instance):
        self.manager.current = "products"

    def navigate_to_customers(self, instance):
        self.manager.current = "customers"

    def navigate_to_orders(self, instance):
        self.manager.current = "orders"

# Product Management Screen
class ProductsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        add_product_button = Button(text="Add Product")
        add_product_button.bind(on_press=self.navigate_to_add_product)

        view_products_button = Button(text="View Products")
        view_products_button.bind(on_press=self.navigate_to_view_products)

        back_button = Button(text="Back to Home")
        back_button.bind(on_press=self.navigate_to_home)

        layout.add_widget(add_product_button)
        layout.add_widget(view_products_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    # Add a method to navigate to the Products screen
    def navigate_to_products(self, instance):
        self.manager.current = "products"

    def navigate_to_add_product(self, instance):
        self.manager.current = "add_product"

    def navigate_to_view_products(self, instance):
        self.manager.current = "view_products"

    def navigate_to_home(self, instance):
        self.manager.current = "home"

    def view_products(self, instance):
        response = requests.get(API_BASE_URL)
        if response.status_code == 200:
            products = response.json()
            products_list = "\n".join(
                [f"ID: {p['id']}, Name: {p['name']}, Price: {p['price']}, Quantity: {p['quantity']}" for p in products]
            )
            products_screen = Screen(name="view_products")
            layout = BoxLayout(orientation="vertical")
            label = Label(text=products_list, size_hint_y=None, height=500)
            layout.add_widget(label)
            back_button = Button(text="Back to Products")
            back_button.bind(on_press=self.navigate_to_products)
            layout.add_widget(back_button)
            products_screen.add_widget(layout)
            self.manager.add_widget(products_screen)
            self.manager.current = "view_products"
        else:
            print("Failed to retrieve products")

# Add Product Screen
class AddProductScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.name_input = TextInput(hint_text="Product Name", multiline=False)
        self.price_input = TextInput(hint_text="Product Price", multiline=False)
        self.quantity_input = TextInput(hint_text="Product Quantity", multiline=False)

        add_button = Button(text="Add Product")
        add_button.bind(on_press=self.add_product)

        back_button = Button(text="Back to Products")
        back_button.bind(on_press=self.navigate_to_products)

        layout.add_widget(self.name_input)
        layout.add_widget(self.price_input)
        layout.add_widget(self.quantity_input)
        layout.add_widget(add_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def add_product(self, instance):
        name = self.name_input.text
        price = self.price_input.text
        quantity = self.quantity_input.text
        
        if not name or not price or not quantity:
            print("All fields are required.")
            return

        try:
            data = {
                "name": name,
                "price": float(price),
                "quantity": int(quantity)
            }
            response = requests.post(API_BASE_URL, json=data)
            if response.status_code == 200:
                print("Product added successfully")
                self.navigate_to_products(instance)
            else:
                print("Failed to add product")
        except ValueError:
            print("Invalid price or quantity format.")

    def navigate_to_products(self, instance):
        self.manager.current = "products"

# Customer Management Screen
class CustomersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        add_customer_button = Button(text="Add Customer")
        add_customer_button.bind(on_press=self.navigate_to_add_customer)

        view_customers_button = Button(text="View Customers")
        view_customers_button.bind(on_press=self.navigate_to_view_customers)

        back_button = Button(text="Back to Home")
        back_button.bind(on_press=self.navigate_to_home)

        layout.add_widget(add_customer_button)
        layout.add_widget(view_customers_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def navigate_to_add_customer(self, instance):
        self.manager.current = "add_customer"

    def navigate_to_view_customers(self, instance):
        self.manager.current = "view_customers"

    def navigate_to_home(self, instance):
        self.manager.current = "home"

# Orders Management Screen
class OrdersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        create_order_button = Button(text="Create Order")
        create_order_button.bind(on_press=self.navigate_to_create_order)

        view_orders_button = Button(text="View Orders")
        view_orders_button.bind(on_press=self.navigate_to_view_orders)

        back_button = Button(text="Back to Home")
        back_button.bind(on_press=self.navigate_to_home)

        layout.add_widget(create_order_button)
        layout.add_widget(view_orders_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def navigate_to_create_order(self, instance):
        self.manager.current = "create_order"

    def navigate_to_view_orders(self, instance):
        self.manager.current = "view_orders"

    def navigate_to_home(self, instance):
        self.manager.current = "home"

class ViewProductsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.product_list = ScrollView()
        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.product_list.add_widget(self.layout)
        layout.add_widget(self.product_list)
        
        back_button = Button(text="Back to Products")
        back_button.bind(on_press=self.navigate_to_products)
        layout.add_widget(back_button)

        self.add_widget(layout)
        self.load_products()

    def load_products(self):
        try:
            response = requests.get(API_BASE_URL)
            response.raise_for_status()
            products = response.json()

            self.layout.clear_widgets()
            if products:
                for product in products:
                    product_label = Label(
                        text=f"Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}",
                        size_hint_y=None, height=44
                    )
                    self.layout.add_widget(product_label)
            else:
                self.layout.add_widget(Label(text="No products available."))

        except requests.exceptions.RequestException as e:
            print(f"Error fetching products: {e}")
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text="Failed to load products. Please try again later."))

    def navigate_to_products(self, instance):
        self.manager.current = "products"

# Main App Class
class ManagementApp(App):
    def build(self):
        sm = ScreenManager()

        # Home Screen
        sm.add_widget(HomeScreen(name="home"))

        # Product Management Screens
        sm.add_widget(ProductsScreen(name="products"))
        sm.add_widget(AddProductScreen(name="add_product"))
        sm.add_widget(ViewProductsScreen(name="view_products"))

        # Customer Management Screens
        sm.add_widget(CustomersScreen(name="customers"))

        # Orders Management Screens
        sm.add_widget(OrdersScreen(name="orders"))

        return sm

if __name__ == "__main__":
    ManagementApp().run()
