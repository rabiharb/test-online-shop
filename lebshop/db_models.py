from flask_login import UserMixin
from sqlalchemy.orm import relationship
from lebshop import db


fruit_category_association_table = db.Table(
    'fruit_category_association_table', db.Model.metadata,
    db.Column('fruit_id', db.Integer(), db.ForeignKey('fruits.id')),
    db.Column('categories_id', db.Integer(), db.ForeignKey('categories.id'))
)
# fruit_shopping_cart_association_table = db.Table(
#     'fruit_shopping_cart_association_table', db.Model.metadata,
#     db.Column('fruit_id', db.Integer(), db.ForeignKey('fruits.id')),
#     db.Column('cart_id', db.Integer(), db.ForeignKey('shopping_cart.id')),
#     db.Column('fruit_amount', db.Float())
# )


class FruitCartAss(db.Model):
    __tablename__ = "fruit_shopping_cart_association_table_obj"
    fruit_id = db.Column(db.ForeignKey('fruits.id'), primary_key=True)
    cart_id = db.Column(db.ForeignKey('shopping_cart.id'), primary_key=True)
    fruit_amount = db.Column(db.Float())
    fruit_obj = relationship("Fruit", back_populates="carts")
    cart_obj = relationship("ShoppingCart", back_populates="items")


class CheckOutSessionData(db.Model):
    __tablename__ = "checkout_session_data"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    total_amount = db.Column(db.String(20), nullable=False)
    currency = db.Column(db.String(8), nullable=False)
    session_date = db.Column(db.String(30), nullable=False)
    items_count = db.Column(db.String(9999), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)


class Fruit(db.Model):
    __tablename__ = "fruits"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    uom = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    currency = db.Column(db.String(32), nullable=False)
    in_stock = db.Column(db.Boolean(), nullable=False)
    desc = db.Column(db.String(100))
    image_path = db.Column(db.String(100), unique=True)
    categories = relationship(
        "Categories", secondary=fruit_category_association_table)
    carts = relationship("FruitCartAss", back_populates="fruit_obj")


class Categories(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class ShoppingCart(db.Model):
    __tablename__ = "shopping_cart"
    id = db.Column(db.Integer(), primary_key=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    items = relationship("FruitCartAss", back_populates="cart_obj")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False)
