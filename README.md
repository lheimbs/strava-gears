# strava-gears

Automate setting the used bike/shoe of a given activity based on heuristics.

## Overview

strava-gears is a Python application that uses the Strava API to automatically assign gear (bikes, shoes) to activities based on configurable heuristics and rules.

## Features

- OAuth2 authentication with Strava API
- List recent activities and available gear
- Manual gear assignment to activities
- Automatic gear assignment based on activity type
- Extensible heuristics system for custom rules

## Installation

This project uses uv for dependency management.

```bash
# Clone the repository
git clone https://github.com/lheimbs/strava-gears.git
cd strava-gears

# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

## Configuration

Before using the application, you need to create a Strava API application:

1. Go to https://www.strava.com/settings/api
2. Create a new application
3. Note your Client ID and Client Secret

## Usage

### Authentication

First, authenticate with the Strava API:

```bash
strava-gears auth
```

This will prompt for your Client ID and Client Secret, then open a browser for OAuth2 authentication.

### Check Status

Verify your authentication status:

```bash
strava-gears status
```

### List Activities

View your recent activities:

```bash
strava-gears list-activities --limit 10
```

### List Gear

View your available gear:

```bash
strava-gears list-gear
```

### Assign Gear

Manually assign gear to a specific activity:

```bash
strava-gears assign --activity-id ACTIVITY_ID --gear-id GEAR_ID
```

### Auto-Assign Gear

Automatically assign gear to activities based on type:

```bash
strava-gears auto-assign --activity-type Ride --gear-id GEAR_ID --limit 30
```

Use `--dry-run` to preview changes without applying them:

```bash
strava-gears auto-assign --activity-type Ride --gear-id GEAR_ID --dry-run
```

## Architecture

The project is organized as a modular application with clear separation of concerns:

- `src/strava_gears/core/`: Core API for Strava integration
  - `client.py`: Strava API client wrapper
  - `auth.py`: OAuth2 authentication flow
  - `config.py`: Configuration management
  - `heuristics.py`: Gear assignment rules and heuristics engine
- `src/strava_gears/cli/`: Command-line interface
  - `main.py`: Main CLI entry point
  - `activities.py`: Activity listing commands
  - `assign.py`: Gear assignment commands

The core API is completely independent of the CLI, making it easy to add additional interfaces (such as a web interface) in the future without modifying the core functionality.

## Development

The project uses uv for dependency management and follows a modular architecture to support future extensions.

### Extending Heuristics

The heuristics system is designed to be extensible. You can create custom rules by using the `GearRule` class:

```python
from strava_gears.core import GearRule, GearAssigner

# Create a custom rule
def my_condition(activity):
    return activity.distance > 50000  # 50km

rule = GearRule("Long Ride", my_condition, "my_road_bike_id")

# Use it with the assigner
assigner = GearAssigner()
assigner.add_rule(rule)
```

Built-in rule factories are available:
- `create_activity_type_rule`: Match by activity type (Ride, Run, etc.)
- `create_distance_rule`: Match by distance range
- `create_name_pattern_rule`: Match by activity name pattern

### Adding a Web Interface

The core API is independent of the CLI, making it straightforward to add a web interface:

1. Create a new `src/strava_gears/web/` package
2. Import and use the core API classes
3. The core handles all Strava API interaction and business logic

## License

See LICENSE file for details.
