from http import HTTPStatus
from flasgger import SwaggerView
from webargs.flaskparser import use_args

from core.schemas import LoginSchema
from core.services import LoginService


class LoginView(SwaggerView):
    service = LoginService
    tags = ["auth"]
    definitions = {
        "LoginSchema": LoginSchema,
    }

    @use_args(LoginSchema)
    def post(self, credentials):
        """Endpoint that authenticates a user.
        ---
        parameters:
            -   name: credentials
                in: body
                schema:
                    $ref: '#/definitions/LoginSchema'
        responses:
            200:
                description: Successful login.
                schema:
                    type: object
                    properties:
                        access_token:
                            type: string
            401:
                description: Credentials are invalid.
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            example: 'E-mail or password are invalid.'
            422:
                description: Unprocessable parameters.
        """
        if not self.service.check_credentials(credentials):
            return (
                dict(message="E-mail or password are invalid."),
                HTTPStatus.UNAUTHORIZED,
            )

        access_token = self.service.get_access_token(credentials)
        return dict(access_token=access_token)
