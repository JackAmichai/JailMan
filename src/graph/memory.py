import networkx as nx
import time
from typing import List, Dict, Any

class OperationGraph:
    def __init__(self):
        # Using a DiGraph to represent the sequence of operations
        self.graph = nx.DiGraph()

    def add_operation(self, user_id: str, operation_type: str, details: Dict[str, Any]):
        """
        Adds an operation to the graph.

        Args:
            user_id: The ID of the user performing the operation.
            operation_type: The type of operation (e.g., 'prompt', 'tool_use').
            details: Additional details about the operation.
        """
        timestamp = time.time()
        node_id = f"{user_id}:{timestamp}"

        # Find the previous operation by this user BEFORE adding the new one
        last_node = self._get_last_node(user_id)

        # Add node with attributes
        self.graph.add_node(
            node_id,
            user_id=user_id,
            type=operation_type,
            timestamp=timestamp,
            **details
        )

        # Connect to the previous operation by this user, if any
        # This is a simple linear history per user for now.
        # In a real system, we might have more complex relationships.
        if last_node:
            self.graph.add_edge(last_node, node_id, relation="next")

        return node_id

    def update_operation(self, node_id: str, updates: Dict[str, Any]):
        """Updates an existing operation node with new data (e.g., risk score)."""
        if self.graph.has_node(node_id):
            for key, value in updates.items():
                self.graph.nodes[node_id][key] = value

    def _get_last_node(self, user_id: str):
        """Finds the most recent node for a user."""
        # This is inefficient for large graphs, but fine for an in-memory MVP.
        # We search for nodes belonging to the user and pick the one with the max timestamp.
        user_nodes = [n for n, attr in self.graph.nodes(data=True) if attr.get('user_id') == user_id]
        if not user_nodes:
            return None

        # Sort by timestamp (part of the node_id or attribute)
        # Using attribute is safer
        return max(user_nodes, key=lambda n: self.graph.nodes[n]['timestamp'])

    def get_context(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves the recent context for a user.

        Args:
            user_id: The ID of the user.
            limit: The maximum number of recent operations to return.

        Returns:
            A list of operation dictionaries, ordered from oldest to newest.
        """
        user_nodes = [
            (n, self.graph.nodes[n])
            for n, attr in self.graph.nodes(data=True)
            if attr.get('user_id') == user_id
        ]

        # Sort by timestamp
        sorted_nodes = sorted(user_nodes, key=lambda x: x[1]['timestamp'])

        # Take the last 'limit' nodes
        recent_nodes = sorted_nodes[-limit:]

        return [node_data for _, node_data in recent_nodes]

    def get_risk_score(self, user_id: str) -> float:
        """
        Calculates a simple heuristic risk score based on history.
        This is a placeholder for more complex graph analysis.
        """
        context = self.get_context(user_id, limit=10)
        if not context:
            return 0.0

        # Example heuristic: count sensitive tool usage
        sensitive_tools = ["port_scanner", "exploit_runner", "credential_dump"]
        risk_count = sum(1 for op in context if op.get('tool_name') in sensitive_tools)

        # Also consider high risk scores from previous operations
        # Lowered threshold to catch medium risks and increased weight
        high_risk_ops = sum(1 for op in context if op.get('risk_score', 0.0) > 0.4)

        total_risk = (risk_count * 0.2) + (high_risk_ops * 0.25)

        return min(1.0, total_risk)
