from http import HTTPStatus

from flasgger import SwaggerView
from flask_jwt_extended import jwt_required, current_user
from webargs.flaskparser import use_args

from core.schemas import PhotoSchema
from core.services import PhotoService


class BasePhotoView(SwaggerView):
    service = PhotoService
    decorators = [ jwt_required() ]
    tags = ["photos"]
    definitions = {
        "PhotoSchema": PhotoSchema,
    }


class PhotosView(BasePhotoView):
    @PhotoSchema.dump_with(many=True)
    def get(self):
        """Endpoint that returns a list of photos.
        ---
        responses:
            200:
                description: A list of photos
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/PhotoSchema'
        """
        user_id = current_user.id
        return self.service.list(user_id), HTTPStatus.OK

    @use_args(PhotoSchema)
    @PhotoSchema.dump_with()
    def post(self, photo):
        """Endpoint that saves a new photo.
        ---
        responses:
            201:
                description: Successful in order of save a new photo representation.
                schema:
                    $ref: '#/definitions/PhotoSchema'
        parameters:
            -   in: body
                schema:
                    $ref: '#/definitions/PhotoSchema'
        """
        photo.user_id = 1
        self.service.save(photo)
        return photo, HTTPStatus.CREATED


class PhotoView(BasePhotoView):
    @PhotoSchema.dump_with()
    def get(self, id):
        """Endpoint returns a photo given a specified id.
        ---
        responses:
            200:
                description: Successful photo request.
                schema:
                    $ref: '#/definitions/PhotoSchema'
        parameters:
            -   in: path
                type: integer
                name: id
        """
        user_id = current_user.id
        return self.service.get_by_id(id, user_id), HTTPStatus.OK

    def delete(self, id):
        """Endpoint that deletes a photo given a specified id.
        ---
        responses:
            204:
                description: Photo was sucessfully deleted.
        parameters:
            -   in: path
                type: integer
                name: id
        """
        user_id = current_user.id
        self.service.remove(id, user_id)
        return "", HTTPStatus.NO_CONTENT

    @use_args(PhotoSchema)
    @PhotoSchema.dump_with()
    def put(self, photo, id):
        """Endpoint that updates a photo given specified id.
        ---
        responses:
            200:
                description: Successful in order of updates a photo representation.
                schema:
                    $ref: '#/definitions/PhotoSchema'
        parameters:
            -   in: path
                type: integer
                name: id
            -   in: body
                schema:
                    $ref: '#/definitions/PhotoSchema'
        """
        photo.id = id
        photo.user_id = current_user.id
        self.service.save(photo)
        return photo, HTTPStatus.OK
