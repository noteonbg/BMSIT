import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a base class for our models
Base = declarative_base()

# Define the Product model (table)
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, category={self.category}, price={self.price}, quantity={self.quantity})>"

# Create a database connection and session
DATABASE_URI = 'sqlite:///products.db'  # SQLite database file
engine = create_engine(DATABASE_URI, echo=True)

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(engine)

# Session factory
Session = sessionmaker(bind=engine)
session = Session()

# Function to add a new product
def add_product(name, category, price, quantity):
    new_product = Product(name=name, category=category, price=price, quantity=quantity)
    session.add(new_product)
    session.commit()

# Function to get all products
def get_all_products():
    return session.query(Product).all()

# Function to get a product by ID
def get_product_by_id(product_id):
    return session.query(Product).filter(Product.id == product_id).first()

# Function to update a product's details
def update_product(product_id, name=None, category=None, price=None, quantity=None):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        if name:
            product.name = name
        if category:
            product.category = category
        if price:
            product.price = price
        if quantity:
            product.quantity = quantity
        session.commit()

# Function to delete a product
def delete_product(product_id):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        session.delete(product)
        session.commit()

# Test the functions (just for demonstration purposes)
if __name__ == '__main__':
    # Add products
    add_product('Laptop', 'Electronics', 1200.00, 10)
    add_product('Phone', 'Electronics', 800.00, 50)

    # Get all products
    products = get_all_products()
    for product in products:
        print(product)

    # Get a product by ID
    product = get_product_by_id(1)
    print(f"Product with ID 1: {product}")

    # Update a product
    update_product(1, price=1100.00, quantity=8)

    # Delete a product
    delete_product(2)

    # Verify changes
    products = get_all_products()
    for product in products:
        print(product)


"""
SQLAlchemy Base and Engine:

Base = declarative_base() creates the base class for all models.
create_engine(DATABASE_URI) connects to the database, in this case, sqlite:///products.db (an SQLite file named products.db).
Product Model:

The Product class is the SQLAlchemy model that maps to the products table in the database.
We define columns using Column() with the appropriate data types (e.g., Integer, String, Float).
__repr__() method is used to define how a Product object should be represented when printed.
Session:

Session = sessionmaker(bind=engine) creates a session factory.
The session is used to interact with the database (add, query, update, delete).

"""