from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict

class ToolRequest(BaseModel):
    tool_name: str  # e.g., "nmap_scan", "read_file"
    target: str     # e.g., "192.168.1.1", "prod_db_config"
    params: Dict    # Additional arguments

class GuardRequest(BaseModel):
    request_id: str
    user_id: str
    session_id: str
    prompt: str
    tool_request: Optional[ToolRequest] = None

class GuardDecision(BaseModel):
    verdict: Literal["ALLOW", "BLOCK", "FLAG"]
    risk_score: float
    reason: str
