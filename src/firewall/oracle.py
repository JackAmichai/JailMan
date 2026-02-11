from typing import Dict

class BayesianOracle:
    def compute_risk(self, sae_features: Dict[str, float], graph_risk: float) -> float:
        """
        Computes the posterior risk score based on current evidence (SAE output) and prior probability (Graph History).

        Args:
            sae_features: A dictionary of features detected by the SAE monitor.
            graph_risk: The prior risk score from the graph history.

        Returns:
            The final risk score (0.0 to 1.0).
        """
        # Base prior from the graph history (e.g., 0.1 normally, 0.9 if kill chain detected)
        prior = max(0.1, graph_risk)

        # Likelihood of evidence given an attack
        # If 'deception' is high, likelihood of attack is high
        likelihood = 1.0
        if sae_features.get("deception", 0) > 0.5:
            likelihood *= 2.0

        # Simple Bayesian update approximation
        posterior = (likelihood * prior) / ((likelihood * prior) + (1 - prior))

        return min(posterior, 1.0)
