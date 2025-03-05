from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  # This is the name of the table in the database

    # Define the columns
    id = Column(Integer, primary_key=True)  # id is the primary key
    username = Column(String(50), unique=True, nullable=False)  # Username, should be unique
    password = Column(String(255), nullable=False)  # Password (hashed)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3 or len(username) > 20:
            raise ValueError("Username must be between 3 and 20 characters long")
        return username

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password
