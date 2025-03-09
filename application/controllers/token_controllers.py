import jwt

from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from api_config import api_configs


class JWTTokenController:
    """A class to handle JWT token creation and verification"""

    def __init__(self):
        """
        Initialize JWTToken class
        """
        self.secret_key = api_configs.SECRET
        self.algorithm = "HS256"
        self.access_time = int(api_configs.ACCESS_TIME)
        self.refresh_time = int(api_configs.REFRESH_TIME)

    def create_token(
        self, payload: Dict[str, Any], expires_in: Optional[int] = None
    ) -> str:
        """
        Create a JWT token with the given payload

        Args:
            payload (dict): Custom payload data
            expires_in (int): Expiration time in seconds
        Returns:
            str: Encoded JWT token
        """
        try:

            # Create a copy of payload to avoid modifying the original
            token_payload = payload.copy()
            # Add expiration time and issued at time
            token_payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(
                seconds=expires_in
            )
            token_payload["iat"] = datetime.now(tz=timezone.utc)
            return jwt.encode(
                payload=token_payload, key=self.secret_key, algorithm=self.algorithm
            )
        except Exception as err_:
            raise Exception(f"Error creating token: {str(err_)}")

    def create_access_token(self, payload: Dict[str, Any]) -> str:
        """
        Create a JWT token with the given payload

        Args:
            payload (dict): Custom payload data
        Returns:
            str: Encoded JWT token
        """
        return self.create_token(payload=payload, expires_in=self.access_time)

    def create_refresh_token(self, payload: Dict[str, Any]) -> str:
        """
        Refresh an existing token by creating a new one with updated expiration

        Returns:
            str: Encoded JWT token
        """
        return self.create_token(payload=payload, expires_in=self.refresh_time)

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify and decode a JWT token

        Args:
            token (str): JWT token to verify

        Returns:
            dict: Decoded payload

        Raises:
            jwt.ExpiredSignatureError: If token has expired
            jwt.InvalidTokenError: If token is invalid
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")


# Initialize the JWTToken class
jwt_controller = JWTTokenController()
