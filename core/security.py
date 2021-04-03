from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .models import UserModel

from .services import UserService

jwt = JWTManager()
cors = CORS(
    resources={
        r"/api/*": {
            "origins": "*",
        }
    }
)

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_callback(user: UserModel) -> int:
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data) -> UserModel:
    identity = jwt_data['sub']
    return UserService.get_by_id(identity)
