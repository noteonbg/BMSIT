import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, OperationalError

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

# Function to add a new product
def add_product(name, category, price, quantity):
    session = Session()
    try:
        new_product = Product(name=name, category=category, price=price, quantity=quantity)
        session.add(new_product)
        session.commit()
        print(f"Product '{name}' added successfully.")
    except IntegrityError as e:
        session.rollback()
        print(f"Error: Integrity error occurred while adding product. {e}")
    except OperationalError as e:
        session.rollback()
        print(f"Error: Operational error occurred. {e}")
    except Exception as e:
        session.rollback()
        print(f"Unexpected error occurred: {e}")
    finally:
        session.close()

# Function to get all products
def get_all_products():
    session = Session()
    try:
        products = session.query(Product).all()
        return products
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []
    finally:
        session.close()

# Function to get a product by ID
def get_product_by_id(product_id):
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            return product
        else:
            print(f"No product found with ID {product_id}")
            return None
    except Exception as e:
        print(f"Error fetching product with ID {product_id}: {e}")
        return None
    finally:
        session.close()

# Function to update a product's details
def update_product(product_id, name=None, category=None, price=None, quantity=None):
    session = Session()
    try:
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
            print(f"Product with ID {product_id} updated successfully.")
        else:
            print(f"No product found with ID {product_id}")
    except IntegrityError as e:
        session.rollback()
        print(f"Error: Integrity error occurred while updating product. {e}")
    except OperationalError as e:
        session.rollback()
        print(f"Error: Operational error occurred. {e}")
    except Exception as e:
        session.rollback()
        print(f"Unexpected error occurred: {e}")
    finally:
        session.close()

# Function to delete a product
def delete_product(product_id):
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            session.delete(product)
            session.commit()
            print(f"Product with ID {product_id} deleted successfully.")
        else:
            print(f"No product found with ID {product_id}")
    except OperationalError as e:
        session.rollback()
        print(f"Error: Operational error occurred. {e}")
    except Exception as e:
        session.rollback()
        print(f"Unexpected error occurred: {e}")
    finally:
        session.close()

# Test the functions (just for demonstration purposes)
if __name__ == '__main__':
    # Add products
    add_product('Laptop', 'Electronics', 1200.00, 10)
    add_product('Phone', 'Electronics', 800.00, 50)

    # Get all products
    products = get_all_products()
    if products:
        for product in products:
            print(product)

    # Get a product by ID
    product = get_product_by_id(1)
    if product:
        print(f"Product with ID 1: {product}")

    # Update a product
    update_product(1, price=1100.00, quantity=8)

    # Delete a product
    delete_product(2)

    # Verify changes
    products = get_all_products()
    if products:
        for product in products:
            print(product)
