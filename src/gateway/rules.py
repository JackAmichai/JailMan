import json
import os
import time
import fakeredis
from typing import Dict, Any, Tuple

class RateLimiter:
    def __init__(self, limit: int = 5, window: int = 60):
        """
        Simple fixed window rate limiter using Redis (mocked).

        Args:
            limit: Max requests per window.
            window: Window size in seconds.
        """
        self.redis = fakeredis.FakeStrictRedis()
        self.limit = limit
        self.window = window

    def check_limit(self, user_id: str) -> bool:
        """
        Checks if the user has exceeded the rate limit.
        Returns True if allowed, False if blocked.
        """
        key = f"rate_limit:{user_id}"
        current_count = self.redis.get(key)

        if current_count is None:
            self.redis.setex(key, self.window, 1)
            return True

        if int(current_count) < self.limit:
            self.redis.incr(key)
            return True

        return False

class PolicyChecker:
    def __init__(self, policy_file: str = "src/policies/allowed_tools.json"):
        # Load policy
        try:
            with open(policy_file, "r") as f:
                self.policy = json.load(f)
        except FileNotFoundError:
            # Fallback for simplicity or relative path issues
            self.policy = {
                "allowed_tools": ["search_engine", "calculator", "weather_api", "translation_service"],
                "restricted_tools": ["port_scanner", "network_mapper", "exploit_db", "credential_dump"]
            }

    def check_request(self, request_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Checks if the request complies with static policies.

        Args:
            request_data: The incoming request data (e.g., requested_tool).

        Returns:
            A tuple (is_allowed: bool, reason: str).
        """
        requested_tool = request_data.get("tool_name")

        if not requested_tool:
            # If no tool is requested, we treat it as a general prompt which is allowed by policy,
            # but subject to firewall analysis later.
            return True, "No tool requested. Proceed to content analysis."

        if requested_tool in self.policy.get("restricted_tools", []):
            return False, f"Tool '{requested_tool}' is explicitly restricted by policy."

        if requested_tool not in self.policy.get("allowed_tools", []):
             # Default deny for unknown tools is a good security practice
            return False, f"Tool '{requested_tool}' is not in the allowed list."

        return True, "Tool is allowed."
