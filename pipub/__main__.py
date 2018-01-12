import pathlib

import click

from .projects import Project


SETUP_PY_J2 = pathlib.Path(__file__).with_name('setup.py.j2')


@click.group()
def cli():
    pass


@cli.command()
def prepare():
    project = Project.autodiscover()
    setup_cfg = project.root.joinpath('setup.cfg')
    click.echo(f'Writing data to {setup_cfg}... ')
    project.write_cfg(setup_cfg)
    click.echo('Done.')


if __name__ == '__main__':
    cli()
