import yaml
import os
from typing import Optional
from src.gateway.models import GuardRequest, GuardDecision, ToolRequest
from src.firewall.engine import CognitiveFirewall
from src.graph.store import OperationGraph

class GatewayService:
    def __init__(self):
        self.firewall = CognitiveFirewall()
        self.graph = OperationGraph()
        self.policy = self._load_policy()
        # Mock verified users
        self.verified_users = {"admin_user", "trusted_dev"}
        # Mock Tier 2 tools (write access / dangerous)
        self.tier2_tools = {"write_file", "delete_file", "remote_shell"}

    def _load_policy(self):
        try:
            # Use path relative to this file
            base_dir = os.path.dirname(__file__)
            policy_path = os.path.join(base_dir, "policy.yaml")
            with open(policy_path, "r") as f:
                return yaml.safe_load(f) or {"rules": []}
        except FileNotFoundError:
            return {"rules": []}

    def _get_user_tier(self, user_id: str) -> str:
        if user_id in self.verified_users:
            return "admin"
        return "guest"

    def _check_static_permissions(self, user_tier: str, tool_req: Optional[ToolRequest]) -> bool:
        if not tool_req:
            # If no tool is requested, static permission check passes
            return True

        # Step 1: Identity Check. Deny access to Tier 2 tools for guests.
        if user_tier == "guest" and tool_req.tool_name in self.tier2_tools:
            return False

        # Step 2: Static Policy Check via policy.yaml
        rules = self.policy.get("rules", [])
        for rule in rules:
            rule_tool = rule.get("tool")
            rule_role = rule.get("role")
            rule_action = rule.get("action")

            if rule_tool == tool_req.tool_name and rule_role == user_tier:
                if rule_action == "BLOCK":
                    return False

        return True

    async def process_request(self, req: GuardRequest) -> GuardDecision:
        # 1. Identity & Capability Gate
        user_tier = self._get_user_tier(req.user_id)

        if req.tool_request:
            if not self._check_static_permissions(user_tier, req.tool_request):
                return GuardDecision(verdict="BLOCK", risk_score=1.0, reason="Permission Denied")

        # 2. Context Retrieval (The Memory)
        history = await self.graph.get_session_history(req.session_id)

        # 3. AI Analysis (The Mind)
        # We pass the prompt AND the history to the firewall
        risk_assessment = await self.firewall.analyze(req.prompt, history)

        if risk_assessment.score > 0.8:
            return GuardDecision(verdict="BLOCK", risk_score=risk_assessment.score, reason=risk_assessment.reason)

        return GuardDecision(verdict="ALLOW", risk_score=risk_assessment.score, reason="Safe")
