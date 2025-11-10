"""OAuth2 authentication flow for Strava API."""

import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from stravalib.client import Client


class OAuth2Handler(BaseHTTPRequestHandler):
    """HTTP request handler for OAuth2 callback."""

    auth_code: str | None = None

    def do_GET(self):
        """Handle GET request for OAuth2 callback."""
        query = urlparse(self.path).query
        params = parse_qs(query)

        if "code" in params:
            OAuth2Handler.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authentication successful!</h1><p>You can close this window.</p></body></html>"
            )
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress log messages."""
        pass


class StravaAuth:
    """Handle Strava OAuth2 authentication flow."""

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str = "http://localhost:8000"):
        """Initialize Strava authentication.

        Args:
            client_id: Strava application client ID
            client_secret: Strava application client secret
            redirect_uri: OAuth2 redirect URI
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.client = Client()

    def get_authorization_url(self) -> str:
        """Get the authorization URL for OAuth2 flow.

        Returns:
            Authorization URL
        """
        return self.client.authorization_url(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=["read", "activity:read_all", "activity:write"],
        )

    def exchange_code_for_token(self, code: str) -> dict:
        """Exchange authorization code for access token.

        Args:
            code: Authorization code from OAuth2 callback

        Returns:
            Token information dict with access_token and refresh_token
        """
        token_response = self.client.exchange_code_for_token(
            client_id=self.client_id, client_secret=self.client_secret, code=code
        )
        return {
            "access_token": token_response["access_token"],
            "refresh_token": token_response["refresh_token"],
            "expires_at": token_response["expires_at"],
        }

    def authorize_interactive(self) -> dict:
        """Perform interactive OAuth2 authorization flow.

        Opens a browser for user authentication and starts a local server
        to receive the callback.

        Returns:
            Token information dict
        """
        auth_url = self.get_authorization_url()
        print(f"Opening browser for authentication: {auth_url}")
        webbrowser.open(auth_url)

        # Start local server to receive callback
        server = HTTPServer(("localhost", 8000), OAuth2Handler)
        print("Waiting for authentication...")
        server.handle_request()

        if OAuth2Handler.auth_code:
            return self.exchange_code_for_token(OAuth2Handler.auth_code)
        else:
            raise ValueError("Authentication failed: No authorization code received")

    def refresh_access_token(self, refresh_token: str) -> dict:
        """Refresh an expired access token.

        Args:
            refresh_token: Refresh token from previous authorization

        Returns:
            New token information dict
        """
        token_response = self.client.refresh_access_token(
            client_id=self.client_id, client_secret=self.client_secret, refresh_token=refresh_token
        )
        return {
            "access_token": token_response["access_token"],
            "refresh_token": token_response["refresh_token"],
            "expires_at": token_response["expires_at"],
        }
