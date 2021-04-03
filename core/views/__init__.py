from flask.blueprints import Blueprint

from .auth import LoginView
from .photo import PhotoView, PhotosView
from .user import UsersView

api_bp = Blueprint("api", __name__, url_prefix="/api")

api_bp.add_url_rule("/login", "login", LoginView.as_view("login"))
api_bp.add_url_rule("/users", "users", UsersView.as_view("users"))
api_bp.add_url_rule("/photos", "photos", PhotosView.as_view("photos"))
api_bp.add_url_rule("/photos/<id>", "photo", PhotoView.as_view("photo"))
