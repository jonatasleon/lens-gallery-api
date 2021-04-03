from .db import db_cli
from .user import user_cli
from .photo import photo_cli

command_groups = [
    db_cli,
    photo_cli,
    user_cli,
]
