"""Command-line interface for strava-gears."""

import click

from strava_gears.cli.activities import list_activities, list_gear
from strava_gears.cli.assign import assign_gear, auto_assign
from strava_gears.core import Config, StravaAuth, StravaClient


@click.group()
@click.pass_context
def cli(ctx):
    """Automate gear assignment for Strava activities."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config()


@cli.command()
@click.option("--client-id", prompt=True, help="Strava API client ID")
@click.option("--client-secret", prompt=True, hide_input=True, help="Strava API client secret")
@click.pass_context
def auth(ctx, client_id, client_secret):
    """Authenticate with Strava API."""
    config = ctx.obj["config"]
    config.set_client_credentials(client_id, client_secret)

    auth_client = StravaAuth(client_id, client_secret)
    try:
        tokens = auth_client.authorize_interactive()
        config.set_access_token(tokens["access_token"], tokens["refresh_token"], tokens["expires_at"])
        click.echo("Authentication successful!")
    except Exception as e:
        click.echo(f"Authentication failed: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.pass_context
def status(ctx):
    """Check authentication status."""
    config = ctx.obj["config"]
    client_id, client_secret = config.get_client_credentials()
    access_token = config.get_access_token()

    if not client_id or not client_secret:
        click.echo("Not configured. Run 'strava-gears auth' first.")
        return

    if not access_token:
        click.echo("Not authenticated. Run 'strava-gears auth' to authenticate.")
        return

    try:
        client = StravaClient(access_token)
        athlete = client.get_athlete()
        click.echo(f"Authenticated as: {athlete.firstname} {athlete.lastname}")
    except Exception as e:
        click.echo(f"Authentication error: {e}", err=True)
        click.echo("Please run 'strava-gears auth' to re-authenticate.")


# Register commands from other modules
cli.add_command(list_activities, name="list-activities")
cli.add_command(list_gear, name="list-gear")
cli.add_command(assign_gear, name="assign")
cli.add_command(auto_assign, name="auto-assign")


if __name__ == "__main__":
    cli()
