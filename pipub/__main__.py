import pathlib

import click

from .projects import Project


@click.group()
def cli():
    pass


@cli.command()
def prepare():
    project = Project.autodiscover()
    setup_cfg = project.root.joinpath('setup.cfg')
    click.echo('Writing data to {}... '.format(setup_cfg))
    project.write_cfg(setup_cfg)
    click.echo('Done.')


if __name__ == '__main__':
    cli()
