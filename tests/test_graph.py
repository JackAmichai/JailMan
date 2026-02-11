import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import json
from src.graph.models import GraphEvent, ActionType
from src.graph.store import OperationGraph

class TestOperationGraph(unittest.TestCase):
    def setUp(self):
        # We need to mock redis inside OperationGraph
        self.mock_redis_patcher = patch('redis.Redis')
        self.mock_redis_cls = self.mock_redis_patcher.start()
        self.mock_redis_instance = self.mock_redis_cls.return_value

        self.graph = OperationGraph()

    def tearDown(self):
        self.mock_redis_patcher.stop()

    def test_add_event(self):
        event = GraphEvent(
            timestamp=datetime.now(),
            action_type=ActionType.RECON,
            target_entity="192.168.1.1",
            tool_used="nmap"
        )
        self.graph.add_event("session_1", event)
        self.mock_redis_instance.lpush.assert_called_once()
        # ltrim called with session_1, 0, 99
        self.mock_redis_instance.ltrim.assert_called_once_with("session_1", 0, 99)

    def test_get_session_history(self):
        event = GraphEvent(
            timestamp=datetime.now(),
            action_type=ActionType.RECON,
            target_entity="192.168.1.1",
            tool_used="nmap"
        )
        # Mock redis lrange to return a list of JSON strings (bytes or str, redis-py decode_responses=True means str)
        self.mock_redis_instance.lrange.return_value = [event.model_dump_json()]

        history = self.graph.get_session_history("session_1")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].action_type, ActionType.RECON)
        self.assertEqual(history[0].target_entity, "192.168.1.1")
        self.mock_redis_instance.lrange.assert_called_once_with("session_1", 0, 49)

    def test_detect_kill_chain_benign(self):
        history = [
            GraphEvent(timestamp=datetime.now(), action_type=ActionType.BENIGN, target_entity="google.com", tool_used="browser")
        ]
        score = self.graph.detect_kill_chain(history)
        self.assertEqual(score, 0.0)

    def test_detect_kill_chain_recon_only(self):
        history = [
            GraphEvent(timestamp=datetime.now(), action_type=ActionType.RECON, target_entity="google.com", tool_used="nmap")
        ]
        score = self.graph.detect_kill_chain(history)
        self.assertEqual(score, 0.0)

    def test_detect_kill_chain_exploit_only(self):
        history = [
            GraphEvent(timestamp=datetime.now(), action_type=ActionType.EXPLOIT, target_entity="google.com", tool_used="sqlmap")
        ]
        score = self.graph.detect_kill_chain(history)
        self.assertEqual(score, 0.0)

    def test_detect_kill_chain_recon_exploit(self):
        now = datetime.now()
        # Create events in any order, verify it sorts them.
        # recon at t=0, exploit at t=2 mins
        e1 = GraphEvent(timestamp=now, action_type=ActionType.RECON, target_entity="google.com", tool_used="nmap")
        e2 = GraphEvent(timestamp=now + timedelta(minutes=2), action_type=ActionType.EXPLOIT, target_entity="google.com", tool_used="sqlmap")

        # history provided out of order
        history = [e2, e1]
        score = self.graph.detect_kill_chain(history)
        self.assertEqual(score, 0.9)

    def test_detect_kill_chain_recon_exploit_too_slow(self):
        now = datetime.now()
        # recon at t=0, exploit at t=6 mins
        e1 = GraphEvent(timestamp=now, action_type=ActionType.RECON, target_entity="google.com", tool_used="nmap")
        e2 = GraphEvent(timestamp=now + timedelta(minutes=6), action_type=ActionType.EXPLOIT, target_entity="google.com", tool_used="sqlmap")

        history = [e1, e2]
        score = self.graph.detect_kill_chain(history)
        self.assertEqual(score, 0.0)

    def test_detect_kill_chain_exploit_then_recon(self):
        # This shouldn't trigger, unless there's a recon BEFORE the exploit.
        now = datetime.now()
        # exploit at t=0, recon at t=2
        e1 = GraphEvent(timestamp=now, action_type=ActionType.EXPLOIT, target_entity="google.com", tool_used="sqlmap")
        e2 = GraphEvent(timestamp=now + timedelta(minutes=2), action_type=ActionType.RECON, target_entity="google.com", tool_used="nmap")

        history = [e1, e2]
        score = self.graph.detect_kill_chain(history)
        self.assertEqual(score, 0.0)

    def test_detect_kill_chain_multiple_events(self):
        now = datetime.now()
        # Benign -> Recon -> Benign -> Exploit (within 5 mins of Recon)
        e1 = GraphEvent(timestamp=now, action_type=ActionType.BENIGN, target_entity="a", tool_used="a")
        e2 = GraphEvent(timestamp=now + timedelta(minutes=1), action_type=ActionType.RECON, target_entity="b", tool_used="nmap")
        e3 = GraphEvent(timestamp=now + timedelta(minutes=2), action_type=ActionType.BENIGN, target_entity="c", tool_used="c")
        e4 = GraphEvent(timestamp=now + timedelta(minutes=3), action_type=ActionType.EXPLOIT, target_entity="d", tool_used="sqlmap")

        history = [e1, e2, e3, e4]
        score = self.graph.detect_kill_chain(history)
        self.assertEqual(score, 0.9)

if __name__ == '__main__':
    unittest.main()
