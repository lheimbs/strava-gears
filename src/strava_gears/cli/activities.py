"""Activity management commands."""

import click

from strava_gears.core import StravaClient


@click.command()
@click.option("--limit", default=10, help="Number of activities to list")
@click.pass_context
def list_activities(ctx, limit):
    """List recent activities."""
    config = ctx.obj["config"]
    access_token = config.get_access_token()

    if not access_token:
        click.echo("Not authenticated. Run 'strava-gears auth' first.", err=True)
        raise click.Abort()

    refresh_token = config.get_refresh_token()
    expires_at = config.get_expires_at()
    try:
        client = StravaClient(access_token, refresh_token, expires_at)
        activities = client.get_activities(limit=limit)

        if not activities:
            click.echo("No activities found.")
            return

        click.echo(f"\nFound {len(activities)} activities:\n")
        for activity in activities:
            gear_name = activity.gear.name if activity.gear else "No gear"
            distance_km = float(activity.distance) / 1000 if activity.distance else 0
            click.echo(f"ID: {activity.id}")
            click.echo(f"  Name: {activity.name}")
            click.echo(f"  Type: {activity.type}")
            click.echo(f"  Distance: {distance_km:.2f} km")
            click.echo(f"  Gear: {gear_name}")
            click.echo()
    except Exception as e:
        click.echo(f"Error listing activities: {e}", err=True)
        raise click.Abort()


@click.command()
@click.pass_context
def list_gear(ctx):
    """List available gear."""
    config = ctx.obj["config"]
    access_token = config.get_access_token()

    if not access_token:
        click.echo("Not authenticated. Run 'strava-gears auth' first.", err=True)
        raise click.Abort()

    refresh_token = config.get_refresh_token()
    expires_at = config.get_expires_at()
    try:
        client = StravaClient(access_token)
        gear_list = client.get_athlete_gear()

        if not gear_list:
            click.echo("No gear found.")
            return

        click.echo("\nAvailable gear:\n")
        for gear in gear_list:
            click.echo(f"ID: {gear.id}")
            click.echo(f"  Name: {gear.name}")
            click.echo(f"  Type: {'Bike' if hasattr(gear, 'frame_type') else 'Shoes'}")
            if hasattr(gear, "distance"):
                distance_km = float(gear.distance) / 1000 if gear.distance else 0
                click.echo(f"  Distance: {distance_km:.2f} km")
            click.echo()
    except Exception as e:
        click.echo(f"Error listing gear: {e}", err=True)
        raise click.Abort()
