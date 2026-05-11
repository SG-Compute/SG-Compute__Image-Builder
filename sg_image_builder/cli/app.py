from typing import Optional

import typer

from sg_image_builder import version as sgi_version

app = typer.Typer(
    name='sgi',
    help='sg-compute image builder - capture, package, publish, load ephemeral EC2 images.',
    no_args_is_help=True,
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'sgi {sgi_version}')
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        '--version',
        '-V',
        callback=_version_callback,
        is_eager=True,
        help='Show version and exit.',
    ),
) -> None:
    """Top-level callback. Sub-commands are registered as the package grows."""


@app.command('version')
def version_command() -> None:
    """Print the installed sgi version."""
    typer.echo(f'sgi {sgi_version}')


@app.command('doctor')
def doctor_command() -> None:
    """Diagnose the local environment. Stub in M0; full check lands in M2."""
    typer.echo(f'sgi {sgi_version}')
    typer.echo('doctor: M0 bootstrap - full diagnostics land in M2.')


if __name__ == '__main__':  # pragma: no cover
    app()
