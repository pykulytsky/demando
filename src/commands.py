import time

import typer
from sqlalchemy.engine import reflection

from base.database import engine
from tests.test_database import engine as test_engine

manager = typer.Typer()


@manager.command()
def truncate_db():
    total = 0

    insp = reflection.Inspector.from_engine(engine)
    total_tables = insp.get_table_names()[::-1]

    con = engine.connect()

    typer.echo("\n")
    with typer.progressbar(total_tables, fill_char="█") as progress:
        for table in progress:
            if table != "alembic_version":
                con.execute(f"DELETE FROM {table} CASCADE;")
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
            if table != "alembic_version":
                con.execute(f"DELETE FROM {table} CASCADE;")
                time.sleep(0.3)
                total += 1
        typer.echo(f"Truncated {total} tables.")


@manager.command()
def test():
    with typer.progressbar(range(100), fill_char="█") as progress:
        for _ in progress:
            time.sleep(0.5)


if __name__ == "__main__":
    manager()
