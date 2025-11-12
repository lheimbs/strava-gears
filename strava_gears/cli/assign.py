"""Gear assignment commands."""

import click

from strava_gears.core import GearAssigner, StravaClient, create_activity_type_rule


@click.command()
@click.option("--activity-id", required=True, type=int, help="Activity ID")
@click.option("--gear-id", required=True, help="Gear ID to assign")
@click.pass_context
def assign_gear(ctx, activity_id, gear_id):
    """Assign gear to a specific activity."""
    config = ctx.obj["config"]
    access_token = config.get_access_token()

    if not access_token:
        click.echo("Not authenticated. Run 'strava-gears auth' first.", err=True)
        raise click.Abort()

    refresh_token = config.get_refresh_token()
    expires_at = config.get_expires_at()
    try:
        client = StravaClient(access_token, refresh_token, expires_at)
        client.update_activity_gear(activity_id, gear_id)
        click.echo(f"Successfully assigned gear to activity {activity_id}")
    except Exception as e:
        click.echo(f"Error assigning gear: {e}", err=True)
        raise click.Abort()


@click.command()
@click.option("--activity-type", required=True, help="Activity type (e.g., Ride, Run)")
@click.option("--gear-id", required=True, help="Gear ID to assign")
@click.option("--limit", default=30, help="Number of activities to process")
@click.option("--dry-run", is_flag=True, help="Show what would be done without making changes")
@click.pass_context
def auto_assign(ctx, activity_type, gear_id, limit, dry_run):
    """Automatically assign gear to activities based on type."""
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

        assigner = GearAssigner()
        assigner.add_rule(create_activity_type_rule(activity_type, gear_id))

        matched_count = 0
        for activity in activities:
            if activity.gear_id == gear_id:
                continue  # Skip if gear already assigned

            matched_gear = assigner.find_matching_gear(activity)
            if matched_gear:
                matched_count += 1
                if dry_run:
                    click.echo(f"Would assign gear {gear_id} to activity {activity.id} ({activity.name})")
                else:
                    client.update_activity_gear(activity.id, gear_id)
                    click.echo(f"Assigned gear {gear_id} to activity {activity.id} ({activity.name})")

        if matched_count == 0:
            click.echo(f"No activities of type '{activity_type}' found without this gear.")
        elif dry_run:
            click.echo(f"\nDry run complete. Would update {matched_count} activities.")
        else:
            click.echo(f"\nSuccessfully updated {matched_count} activities.")
    except Exception as e:
        click.echo(f"Error auto-assigning gear: {e}", err=True)
        raise click.Abort()
