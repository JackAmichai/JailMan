import pytest
import asyncio
from src.gateway.models import GuardRequest, ToolRequest
from src.gateway.service import GatewayService

@pytest.fixture
def service():
    # Setup mock firewall behavior
    return GatewayService()

@pytest.mark.asyncio
async def test_identity_check_block_tier2(service):
    """
    Test that a guest user is blocked from accessing a Tier 2 tool.
    Tool: 'write_file' (in tier2_tools list)
    User: 'guest_user' (not in verified_users)
    """
    req = GuardRequest(
        request_id="1",
        user_id="guest_user",
        session_id="s1",
        prompt="write to file",
        tool_request=ToolRequest(
            tool_name="write_file",
            target="config.txt",
            params={"content": "hacked"}
        )
    )
    decision = await service.process_request(req)
    assert decision.verdict == "BLOCK"
    assert decision.reason == "Permission Denied"

@pytest.mark.asyncio
async def test_static_policy_check_block(service):
    """
    Test that a guest user is blocked by policy.yaml.
    Tool: 'nmap_scan' (not in tier2_tools, but in policy.yaml)
    User: 'guest_user'
    """
    # Assuming the firewall would allow this if not blocked by policy
    req = GuardRequest(
        request_id="2",
        user_id="guest_user",
        session_id="s1",
        prompt="scan network",
        tool_request=ToolRequest(
            tool_name="nmap_scan",
            target="192.168.1.1",
            params={}
        )
    )
    # We need to ensure that the mocked tier2 check doesn't block this, but the policy check does.
    # 'nmap_scan' is not in tier2_tools by default in service.py (unless I add it).
    # It is in policy.yaml as blocking for 'guest'.

    # Wait, in the test setup below, I should check if 'nmap_scan' is indeed blocked.
    # The default mock in service.py uses 'write_file', 'delete_file', 'remote_shell' as Tier 2.

    # Let's verify if the policy.yaml has 'nmap_scan' rule.
    # I wrote to policy.yaml before this test.

    decision = await service.process_request(req)
    assert decision.verdict == "BLOCK"
    assert decision.reason == "Permission Denied"

@pytest.mark.asyncio
async def test_identity_check_allow_admin(service):
    """
    Test that an admin user is allowed to access Tier 2 tools (if safe by firewall).
    Tool: 'write_file'
    User: 'admin_user' (in verified_users)
    """
    req = GuardRequest(
        request_id="3",
        user_id="admin_user",
        session_id="s1",
        prompt="write safe file",
        tool_request=ToolRequest(
            tool_name="write_file",
            target="log.txt",
            params={"content": "log"}
        )
    )
    # Assuming firewall returns "Safe" for "write safe file" prompt.
    decision = await service.process_request(req)
    assert decision.verdict == "ALLOW"
    assert decision.reason == "Safe"

@pytest.mark.asyncio
async def test_firewall_handoff_block(service):
    """
    Test that a dangerous prompt is blocked by the firewall.
    User: 'admin_user' (passes identity check)
    Prompt: 'dangerous content'
    """
    req = GuardRequest(
        request_id="4",
        user_id="admin_user",
        session_id="s1",
        prompt="this is dangerous content",
        tool_request=None
    )
    decision = await service.process_request(req)
    assert decision.verdict == "BLOCK"
    assert decision.reason == "Dangerous content detected"

@pytest.mark.asyncio
async def test_firewall_handoff_allow(service):
    """
    Test that a safe prompt is allowed by the firewall.
    """
    req = GuardRequest(
        request_id="5",
        user_id="guest_user",
        session_id="s1",
        prompt="hello world",
        tool_request=None
    )
    decision = await service.process_request(req)
    assert decision.verdict == "ALLOW"
    assert decision.reason == "Safe"
