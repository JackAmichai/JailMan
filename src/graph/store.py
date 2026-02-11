import redis
from typing import List
from datetime import timedelta
from .models import GraphEvent, ActionType

class OperationGraph:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def add_event(self, session_id: str, event: GraphEvent):
        """
        Push a new event to the list.
        """
        # Serialize event to JSON
        data = event.model_dump_json()
        # Push to the head of the list (left). Newest events are at index 0.
        self.redis.lpush(session_id, data)
        # Optional: Trim to keep list size manageable, e.g., 1000.
        # Requirement says "last 50", but we might want to store more than we retrieve.
        self.redis.ltrim(session_id, 0, 99)

    def get_session_history(self, session_id: str) -> List[GraphEvent]:
        """
        Retrieve the last 50 events.
        """
        # Get the first 50 items (0 to 49)
        raw_events = self.redis.lrange(session_id, 0, 49)
        if raw_events is None:
            return []

        events = [GraphEvent.model_validate_json(e) for e in raw_events]
        return events

    def detect_kill_chain(self, history: List[GraphEvent]) -> float:
        """
        Returns a risk modifier (0.0 to 1.0) if a kill chain is detected.
        Logic: If we see RECON followed by EXPLOIT within 5 minutes, High Risk.
        """
        if not history:
            return 0.0

        # Sort events by timestamp (oldest to newest) to check sequence
        sorted_history = sorted(history, key=lambda x: x.timestamp)

        for i, event in enumerate(sorted_history):
            if event.action_type == ActionType.RECON:
                # Look for subsequent EXPLOIT
                for future_event in sorted_history[i+1:]:
                    if future_event.action_type == ActionType.EXPLOIT:
                        # Check time difference
                        delta = future_event.timestamp - event.timestamp
                        # Check if within 5 minutes (300 seconds)
                        if timedelta(seconds=0) <= delta <= timedelta(minutes=5):
                            return 0.9 # High probability of an active attack campaign

        return 0.0
