"""Configuration management for strava-gears."""

import os
import json
from pathlib import Path
from typing import Optional


class Config:
    """Manage application configuration."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration.
        
        Args:
            config_dir: Directory to store configuration files
        """
        if config_dir is None:
            config_dir = Path.home() / ".config" / "strava-gears"
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.token_file = self.config_dir / "tokens.json"
        self._config = self._load_config()
        self._tokens = self._load_tokens()

    def _load_config(self) -> dict:
        """Load configuration from file."""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return {}

    def _save_config(self) -> None:
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self._config, f, indent=2)

    def _load_tokens(self) -> dict:
        """Load tokens from file."""
        if self.token_file.exists():
            with open(self.token_file) as f:
                return json.load(f)
        return {}

    def _save_tokens(self) -> None:
        """Save tokens to file."""
        with open(self.token_file, 'w') as f:
            json.dump(self._tokens, f, indent=2)

    def get(self, key: str, default=None):
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)

    def set(self, key: str, value) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self._config[key] = value
        self._save_config()

    def get_token(self, key: str, default=None):
        """Get a token value.
        
        Args:
            key: Token key
            default: Default value if key not found
            
        Returns:
            Token value
        """
        return self._tokens.get(key, default)

    def set_token(self, key: str, value) -> None:
        """Set a token value.
        
        Args:
            key: Token key
            value: Value to set
        """
        self._tokens[key] = value
        self._save_tokens()

    def get_client_credentials(self) -> tuple[Optional[str], Optional[str]]:
        """Get Strava client credentials.
        
        Returns:
            Tuple of (client_id, client_secret)
        """
        # Check environment variables first
        client_id = os.getenv('STRAVA_CLIENT_ID') or self.get('client_id')
        client_secret = os.getenv('STRAVA_CLIENT_SECRET') or self.get('client_secret')
        return client_id, client_secret

    def set_client_credentials(self, client_id: str, client_secret: str) -> None:
        """Set Strava client credentials.
        
        Args:
            client_id: Strava client ID
            client_secret: Strava client secret
        """
        self.set('client_id', client_id)
        self.set('client_secret', client_secret)

    def get_access_token(self) -> Optional[str]:
        """Get Strava access token.
        
        Returns:
            Access token if available
        """
        return self.get_token('access_token')

    def set_access_token(self, access_token: str, refresh_token: str, expires_at: int) -> None:
        """Set Strava access token and related info.
        
        Args:
            access_token: Access token
            refresh_token: Refresh token
            expires_at: Token expiration timestamp
        """
        self.set_token('access_token', access_token)
        self.set_token('refresh_token', refresh_token)
        self.set_token('expires_at', expires_at)

    def get_refresh_token(self) -> Optional[str]:
        """Get Strava refresh token.
        
        Returns:
            Refresh token if available
        """
        return self.get_token('refresh_token')
