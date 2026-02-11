from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from pathlib import Path

# Adjust path for local execution if needed
import sys
# Ensure the root directory is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.graph.memory import OperationGraph
from src.firewall.analysis import Firewall
from src.gateway.rules import PolicyChecker, RateLimiter

app = FastAPI(title="Neuro-Symbolic AI Guardrail", version="1.0.0")

# Initialize components
graph = OperationGraph()
firewall = Firewall()
# Use robust path for policy file
policy_path = root_dir / "src" / "policies" / "allowed_tools.json"
policy_checker = PolicyChecker(str(policy_path))
rate_limiter = RateLimiter(limit=10, window=60) # 10 req/min for testing

class CheckRequest(BaseModel):
    user_id: str
    prompt: str
    tool_name: Optional[str] = None

class CheckResponse(BaseModel):
    decision: str
    risk_score: float
    reason: str

@app.post("/guard/check", response_model=CheckResponse)
async def check_request(request: CheckRequest):
    """
    Analyzes a user request and returns a decision (ALLOW, BLOCK, MODIFY).
    """
    user_id = request.user_id
    prompt = request.prompt
    tool_name = request.tool_name

    # 0. Gateway: Rate Limiting
    if not rate_limiter.check_limit(user_id):
         graph.add_operation(user_id, "blocked_request", {"reason": "Rate limit exceeded"})
         return CheckResponse(decision="BLOCK", risk_score=1.0, reason="Rate limit exceeded. Try again later.")

    # 1. Gateway: Static Policy Check (The Body)
    is_allowed, policy_reason = policy_checker.check_request({"tool_name": tool_name})

    if not is_allowed:
        # If blocked by static policy, we still log the attempt but return immediately
        graph.add_operation(user_id, "blocked_request", {"prompt": prompt, "tool_name": tool_name, "reason": policy_reason})
        return CheckResponse(decision="BLOCK", risk_score=1.0, reason=policy_reason)

    # 2. Graph: Update Context (The Memory)
    # We add the operation tentatively or mark it as 'pending_analysis'
    # For simplicity, we add it as 'request' and will update status later if needed,
    # or just use the sequence of requests to determine risk.
    node_id = graph.add_operation(user_id, "request", {"prompt": prompt, "tool_name": tool_name})

    # Fetch history-based risk score
    history_risk_score = graph.get_risk_score(user_id)

    # 3. Firewall: Neuro-Symbolic Analysis (The Mind)
    decision, final_score, firewall_reason = firewall.analyze_request(prompt, history_risk_score)

    # 4. Final Decision
    # (The firewall logic already returns the decision, but we could add more logic here)

    # 5. Update Graph with Analysis Result
    graph.update_operation(node_id, {"risk_score": final_score, "decision": decision})

    return CheckResponse(
        decision=decision,
        risk_score=final_score,
        reason=firewall_reason
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
