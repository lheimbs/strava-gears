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

The project is organized as a modular application:

- `src/strava_gears/core/`: Core API for Strava integration
  - `client.py`: Strava API client
  - `auth.py`: OAuth2 authentication
  - `config.py`: Configuration management
  - `heuristics.py`: Gear assignment rules and heuristics
- `src/strava_gears/cli/`: Command-line interface
  - `main.py`: Main CLI entry point
  - `activities.py`: Activity listing commands
  - `assign.py`: Gear assignment commands

## Development

The project uses uv for dependency management and follows a modular architecture to support future extensions (e.g., web interface).

## License

See LICENSE file for details.
