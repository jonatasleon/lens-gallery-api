import click
from flask.cli import AppGroup

from core.db import db
from core.models import PhotoModel as Photo

photo_cli = AppGroup("photo", help="User commands related.")


@photo_cli.command("add")
@click.argument("title")
@click.option("--url", "URL", prompt=True, help="Image URL. Prompted if not defined.")
@click.option(
    "--user-id",
    "user_id",
    type=int,
    prompt=True,
    help="ID code of user that will own the photo. Prompted if not defined.",
)
def add_user(title, url, user_id):
    photo = Photo(title=title, url=url, user_id=user_id)
    db.session.add(photo)
    db.session.commit()
