"""Core API for Strava gear management."""

from strava_gears.core.client import StravaClient
from strava_gears.core.auth import StravaAuth
from strava_gears.core.config import Config
from strava_gears.core.heuristics import (
    GearRule,
    GearAssigner,
    create_activity_type_rule,
    create_distance_rule,
    create_name_pattern_rule,
)

__all__ = [
    "StravaClient",
    "StravaAuth",
    "Config",
    "GearRule",
    "GearAssigner",
    "create_activity_type_rule",
    "create_distance_rule",
    "create_name_pattern_rule",
]
