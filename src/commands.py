from typing import List
import typer
from base.database import engine
from tests.test_database import engine as test_engine
import time
from sqlalchemy.engine import reflection

import asyncio
from functools import wraps

from auth.models import Role
from tortoise import Tortoise


manager = typer.Typer()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@manager.command()
def truncate_db():
    total = 0

    insp = reflection.Inspector.from_engine(engine)
    total_tables = insp.get_table_names()[::-1]

    con = engine.connect()

    typer.echo("\n")
    with typer.progressbar(total_tables, fill_char="█") as progress:
        for table in progress:
            if table != 'alembic_version':
                con.execute(f'DELETE FROM {table} CASCADE;')
                time.sleep(0.3)
                total += 1
        typer.echo(f"Truncated {total} tables.")


@manager.command()
def truncate_test_db():
    total = 0

    insp = reflection.Inspector.from_engine(test_engine)
    total_tables = insp.get_table_names()[::-1]

    con = test_engine.connect()

    typer.echo("\n")
    with typer.progressbar(total_tables, fill_char="█") as progress:
        for table in progress:
            if table != 'alembic_version':
                con.execute(f'DELETE FROM {table} CASCADE;')
                time.sleep(0.3)
                total += 1
        typer.echo(f"Truncated {total} tables.")


@manager.command()
def test():
    with typer.progressbar(range(100), fill_char="█") as progress:
        for _ in progress:
            time.sleep(0.5)


@manager.command()
@coro
async def create_roles():
    await Tortoise.init(config={
        'connections': {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': 'localhost',
                    'port': '5432',
                    'user': 'o_p',
                    'password': '#pragma_once',
                    'database': 'demando',
                },
                'maxsize': 100
            }
        },
        'apps': {
            'auth': {
                'models': ["auth.models"],
                # If no default_connection specified, defaults to 'default'
                'default_connection': 'default',
            }
        }
    },
    )
    with typer.progressbar(range(2), fill_char="█") as progress:
        for i in progress:
            await Role.create(id=i, verbose=f'Role {i}')


if __name__ == '__main__':
    manager()
