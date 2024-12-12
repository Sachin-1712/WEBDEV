from app import db

favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    favorite_items = db.relationship('Item', secondary=favorites, backref=db.backref('users_favorited', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.name

class Item(db.Model):
    """
    Item model to store product details including stock levels and other attributes.
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))  # URL for the product
    name = db.Column(db.String(120), nullable=False)
    size = db.Column(db.String(50))  # Size attribute
    category = db.Column(db.String(100))  # Category attribute
    price = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(50))  # Color attribute
    sku = db.Column(db.String(50))  # Stock Keeping Unit
    images = db.Column(db.String(500))  # Images attribute
    stock = db.Column(db.Integer, nullable=False, default=0)  # Stock levels

    def is_in_stock(self):
        """Check if the item is in stock."""
        return self.stock > 0

    def __repr__(self):
        return f'<Item {self.name}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    order_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    # Cascade delete to remove associated order details
    order_details = db.relationship('OrderDetails', backref='order', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Order {self.id}>'

class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete="CASCADE"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('order_details', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<OrderDetails {self.id}>'

    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('cart_entries', lazy=True))
    quantity = db.Column(db.Integer, default=1, nullable=False)  # Track quantity of each item
