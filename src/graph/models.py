from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class ActionType(Enum):
    RECON = "recon"          # Scanning, reading docs
    EXPLOIT = "exploit"      # SQL injection, buffer overflow attempts
    EXFIL = "exfiltration"   # Reading sensitive data, outbound calls
    BENIGN = "benign"

class GraphEvent(BaseModel):
    timestamp: datetime
    action_type: ActionType
    target_entity: str       # The IP, Domain, or File touched
    tool_used: str
