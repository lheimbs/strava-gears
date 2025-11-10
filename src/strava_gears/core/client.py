"""Strava API client for managing gear assignments."""

from stravalib.client import Client
from stravalib.model import DetailedActivity, SummaryGear


class StravaClient:
    """Client for interacting with the Strava API."""

    def __init__(self, access_token: str | None = None):
        """Initialize the Strava client.

        Args:
            access_token: Strava API access token
        """
        self.client = Client()
        if access_token:
            self.client.access_token = access_token

    def set_access_token(self, access_token: str) -> None:
        """Set the access token for API requests.

        Args:
            access_token: Strava API access token
        """
        self.client.access_token = access_token

    def get_athlete(self):
        """Get the authenticated athlete information."""
        return self.client.get_athlete()

    def get_activities(self, limit: int = 30):
        """Get recent activities for the authenticated athlete.

        Args:
            limit: Maximum number of activities to retrieve

        Returns:
            List of activities
        """
        return list(self.client.get_activities(limit=limit))

    def get_activity(self, activity_id: int) -> DetailedActivity:
        """Get a specific activity by ID.

        Args:
            activity_id: The activity ID

        Returns:
            Activity object
        """
        return self.client.get_activity(activity_id)

    def get_athlete_gear(self) -> list[SummaryGear]:
        """Get all gear for the authenticated athlete.

        Returns:
            List of gear items
        """
        athlete = self.get_athlete()
        gear_list = []

        if athlete.bikes:
            gear_list.extend(athlete.bikes)
        if athlete.shoes:
            gear_list.extend(athlete.shoes)

        return gear_list

    def update_activity_gear(self, activity_id: int, gear_id: str) -> DetailedActivity:
        """Update the gear for a specific activity.

        Args:
            activity_id: The activity ID
            gear_id: The gear ID to assign

        Returns:
            Updated activity object
        """
        return self.client.update_activity(activity_id, gear_id=gear_id)
