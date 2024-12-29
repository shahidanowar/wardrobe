from flask import Blueprint

bp = Blueprint('wardrobe', __name__)

from app.wardrobe import routes
