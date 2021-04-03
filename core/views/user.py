from http import HTTPStatus

from flasgger import SwaggerView
from flask_jwt_extended import current_user, jwt_required
from webargs.flaskparser import use_args

from core.schemas import UserSchema
from core.services import UserService


class BaseUserView(SwaggerView):
    service = UserService
    decorators = [jwt_required(optional=True)]
    tags = ["users"]
    definitions = {
        "UserSchema": UserSchema,
    }


class UsersView(BaseUserView):
    @UserSchema.dump_with()
    def get(self):
        """Endpoint returns authenticated user.
        ---
        responses:
            200:
                description: Authenticated user.
                schema:
                    $ref: '#/definitions/UserSchema'
            401:
                description: Unauthorized by lack of credentials.
        """
        if not current_user:
            return dict(message="Unauthorized by lack of credentials."), HTTPStatus.UNAUTHORIZED
        id = current_user.id
        return self.service.get_by_id(id), HTTPStatus.OK

    @UserSchema.dump_with()
    @use_args(UserSchema)
    def post(self, user):
        """Endpoint creates an user.
        ---
        responses:
            200:
                description: Successfully newly created user.
                schema:
                    $ref: '#/definitions/UserSchema'
            422:
                description: Unprocessable parameters.
        """
        return self.service.save(user), HTTPStatus.CREATED
