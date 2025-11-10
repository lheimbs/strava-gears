"""Heuristics for automatic gear assignment."""

from typing import Optional, Callable
from stravalib.model import SummaryActivity


class GearRule:
    """Represents a rule for assigning gear to activities."""

    def __init__(self, name: str, condition: Callable[[SummaryActivity], bool], gear_id: str):
        """Initialize a gear rule.
        
        Args:
            name: Name of the rule
            condition: Function that returns True if rule applies to activity
            gear_id: Gear ID to assign if condition is met
        """
        self.name = name
        self.condition = condition
        self.gear_id = gear_id

    def matches(self, activity: SummaryActivity) -> bool:
        """Check if this rule matches the given activity.
        
        Args:
            activity: Activity to check
            
        Returns:
            True if rule matches
        """
        return self.condition(activity)


class GearAssigner:
    """Manages gear assignment rules and applies them to activities."""

    def __init__(self):
        """Initialize the gear assigner."""
        self.rules: list[GearRule] = []

    def add_rule(self, rule: GearRule) -> None:
        """Add a gear assignment rule.
        
        Args:
            rule: Rule to add
        """
        self.rules.append(rule)

    def clear_rules(self) -> None:
        """Clear all rules."""
        self.rules.clear()

    def find_matching_gear(self, activity: SummaryActivity) -> Optional[str]:
        """Find the first gear that matches the activity.
        
        Args:
            activity: Activity to match
            
        Returns:
            Gear ID if a match is found, None otherwise
        """
        for rule in self.rules:
            if rule.matches(activity):
                return rule.gear_id
        return None


def create_activity_type_rule(activity_type: str, gear_id: str, name: Optional[str] = None) -> GearRule:
    """Create a rule that matches activities by type.
    
    Args:
        activity_type: Activity type to match (e.g., 'Ride', 'Run')
        gear_id: Gear ID to assign
        name: Optional name for the rule
        
    Returns:
        GearRule instance
    """
    if name is None:
        name = f"Type: {activity_type}"
    return GearRule(name, lambda a: str(a.type) == activity_type, gear_id)


def create_distance_rule(
    min_distance: Optional[float] = None,
    max_distance: Optional[float] = None,
    gear_id: str = "",
    name: Optional[str] = None
) -> GearRule:
    """Create a rule that matches activities by distance.
    
    Args:
        min_distance: Minimum distance in meters
        max_distance: Maximum distance in meters
        gear_id: Gear ID to assign
        name: Optional name for the rule
        
    Returns:
        GearRule instance
    """
    def condition(activity: SummaryActivity) -> bool:
        if activity.distance is None:
            return False
        distance = float(activity.distance)
        if min_distance is not None and distance < min_distance:
            return False
        if max_distance is not None and distance > max_distance:
            return False
        return True

    if name is None:
        name = f"Distance: {min_distance or 0}-{max_distance or 'inf'}"
    return GearRule(name, condition, gear_id)


def create_name_pattern_rule(pattern: str, gear_id: str, name: Optional[str] = None) -> GearRule:
    """Create a rule that matches activities by name pattern.
    
    Args:
        pattern: Pattern to match in activity name (case-insensitive)
        gear_id: Gear ID to assign
        name: Optional name for the rule
        
    Returns:
        GearRule instance
    """
    if name is None:
        name = f"Name contains: {pattern}"
    return GearRule(
        name,
        lambda a: pattern.lower() in (a.name or "").lower(),
        gear_id
    )
