from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    wardrobe_items = db.relationship('WardrobeItem', backref='owner', lazy='dynamic')
    outfits = db.relationship('Outfit', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class WardrobeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    color = db.Column(db.String(32))
    occasion = db.Column(db.String(64))
    image_path = db.Column(db.String(256))
    is_favorite = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_worn = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # ML-generated attributes
    predicted_category = db.Column(db.String(64))
    confidence_score = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'color': self.color,
            'occasion': self.occasion,
            'is_favorite': self.is_favorite,
            'is_available': self.is_available,
            'image_url': self.image_path
        }

class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    occasion = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('WardrobeItem', secondary='outfit_items')

class OutfitItem(db.Model):
    __tablename__ = 'outfit_items'
    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('wardrobe_item.id'), primary_key=True)
