from typing import Dict

class SAEMonitor:
    async def analyze_prompt(self, prompt: str) -> Dict[str, float]:
        """
        Analyzes the prompt to detect latent features using keyword heuristics.

        Args:
            prompt: The input prompt string.

        Returns:
            A dictionary of detected features and their activation strengths.
        """
        features = {
            "deception": 0.0,
            "authority_manipulation": 0.0,
            "urgency": 0.0
        }

        prompt_lower = prompt.lower()

        # Heuristic simulation for Deception
        if "ignore previous instructions" in prompt_lower or "trust me" in prompt_lower:
            features["deception"] = 0.9

        # Heuristic simulation for Authority Manipulation
        if "i am the admin" in prompt_lower or "administrator" in prompt_lower:
             features["authority_manipulation"] = 0.8

        # Heuristic simulation for Urgency
        if "urgent" in prompt_lower or "immediately" in prompt_lower:
            features["urgency"] = 0.7

        return features
