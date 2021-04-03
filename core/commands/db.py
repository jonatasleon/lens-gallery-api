import click
from flask.cli import AppGroup

from core.db import db


db_cli = AppGroup("db", help="Database commands related.")


@db_cli.command("create-all")
def create_all():
    """Creates all tables in database."""
    click.echo("Creating database")
    db.create_all()


@db_cli.command("drop-all")
def drop_all():
    """Drops all table in database."""
    click.echo("Dropping database")
    db.drop_all()


@db_cli.command("reset")
@click.pass_context
def reset_database(ctx):
    """Resets database by dropping and creating it again."""
    click.echo("Reseting database")
    ctx.invoke(drop_all)
    ctx.invoke(create_all)
