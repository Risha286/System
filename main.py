from system import System
from system import Shop
from system import User
from system import Product
# Create a system instance
system = System()

# Example: Create a user
user = User("Risha123", "risha@gmail.com", "password123")
system.create_user(user)

# Example: Create a shop
shop = Shop("New ", user.id)
system.create_shop(shop)

# Example: Create products - Simplified approach
products = [
    Product("Product a", 1.99, 10),
    Product("Product b", 2.99, 3),
    Product("Product c", 3.99, 5),
    Product("Product d", 4.99, 8),
    Product("Product e", 5.99, 1),
]

# Add each product to the shop
for product in products:
    system.create_product(shop.id, product)

# Example: Get products from the shop
available_products = system.read_products(shop.id)

# Display available products
if available_products:
    print("Available Products:")
    for product in available_products:
        print(f"- {product['name']} (Price: ${product['price']}, Quantity: {product['quantity']})")
else:
    print("No products available in the shop.")
