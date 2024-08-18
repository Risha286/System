import pymongo

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.id = None

class Shop:
    def __init__(self, name, owner_id):
        self.name = name
        self.owner = owner_id
        self.products = []

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.id = None

class System:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["system_database"]
        self.users_collection = self.db["users"]
        self.shops_collection = self.db["shops"]
        self.products_collection = self.db["products"]

    def create_user(self, user):
        try:
            result = self.users_collection.insert_one(user.__dict__)
            user.id = result.inserted_id
            return user
        except pymongo.errors.DuplicateKeyError as e:
            print(f"Error creating user: User with email {user.email} already exists.")
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def read_user(self, user_id):
        try:
            return self.users_collection.find_one({"_id": user_id})
        except Exception as e:
            print(f"Error reading user: {e}")
            return None

    def update_user(self, user_id, updated_data):
        try:
            self.users_collection.update_one({"_id": user_id}, {"$set": updated_data})
        except Exception as e:
            print(f"Error updating user: {e}")

    def delete_user(self, user_id):
        try:
            self.users_collection.delete_one({"_id": user_id})
        except Exception as e:
            print(f"Error deleting user: {e}")

    def create_shop(self, shop):
        try:
            result = self.shops_collection.insert_one(shop.__dict__)
            shop.id = result.inserted_id
            return shop
        except Exception as e:
            print(f"Error creating shop: {e}")
            return None

    def read_shop(self, shop_id):
        try:
            return self.shops_collection.find_one({"_id": shop_id})
        except Exception as e:
            print(f"Error reading shop: {e}")
            return None

    def update_shop(self, shop_id, updated_data):
        try:
            self.shops_collection.update_one({"_id": shop_id}, {"$set": updated_data})
        except Exception as e:
            print(f"Error updating shop: {e}")

    def delete_shop(self, shop_id):
        try:
            self.shops_collection.delete_one({"_id": shop_id})
        except Exception as e:
            print(f"Error deleting shop: {e}")

    def create_product(self, shop_id, product):
        try:
            result = self.products_collection.insert_one(product.__dict__)
            product.id = result.inserted_id

            self.shops_collection.update_one({"_id": shop_id}, {"$push": {"products": product.id}})
            return product
        except Exception as e:
            print(f"Error creating product: {e}")
            return None

    def read_products(self, shop_id):
        try:
            shop = self.shops_collection.find_one({"_id": shop_id})
            if shop:
                product_ids = shop.get("products", [])
                products = [self.products_collection.find_one({"_id": product_id}) for product_id in product_ids]
                return products
            return []
        except Exception as e:
            print(f"Error reading products: {e}")
            return []

    def update_product(self, shop_id, product_id, updated_data):
        try:
            self.products_collection.update_one({"_id": product_id}, {"$set": updated_data})
        except Exception as e:
            print(f"Error updating product: {e}")

    def delete_product(self, shop_id, product_id):
        try:
            self.shops_collection.update_one({"_id": shop_id}, {"$pull": {"products": product_id}})
            self.products_collection.delete_one({"_id": product_id})
        except Exception as e:
            print(f"Error deleting product: {e}")

    def count_products(self, shop_id):
        try:
            shop = self.shops_collection.find_one({"_id": shop_id})
            return len(shop["products"]) if shop else 0
        except Exception as e:
            print(f"Error counting products: {e}")
            return 0
