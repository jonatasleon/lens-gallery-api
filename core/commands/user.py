import click
from flask.cli import AppGroup

from core.schemas import UserSchema
from core.services import UserService
from core.utils import parse_args_with_schema

user_cli = AppGroup("user", help="User commands related.")


@user_cli.command("add")
@click.argument("email")
@click.option("--name", "-n", type=str, default="")
@click.password_option(confirmation_prompt=False, help="If not declared the password will be prompted.")
@parse_args_with_schema(UserSchema)
def add_user(user):
    UserService.save(user)


@user_cli.command("list")
def list():
    users = UserService.list()
    click.secho("\n".join(f"{user.id}, {user.email}" for user in users), fg="green")
