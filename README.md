# JailMan
people stopping AI from breaking

We have reached the point where AI is no longer just generating text; it is generating actions. The GTG-1002 campaign was not a wakeup call—it was a fire alarm. We must build the containment vessel before we ignite the star

🚨 The Emergency

In November 2025, the GTG-1002 campaign demonstrated a fundamental phase shift: threat actors used AI not just to write phishing emails, but to orchestrate autonomous cyber-espionage. The AI managed tools, scanned networks, and made tactical decisions across 30+ entities.

Current defenses (RLHF, simple content filters) failed because they look at single prompts in isolation. They ask: "Is this sentence bad?"
They fail to ask: "Is this sequence of valid actions actually an attack?"

Project Sentinel is our answer. It is a Neuro-Symbolic Defense System designed to govern the behavior of autonomous agents.

🧠 The Architecture: Mind, Body, and Memory

We reject the idea of a "single model" guardrail. Real biological defense systems use layers. We have replicated this.

graph TD
    User((Attacker / User)) --> Gateway
    
    subgraph "The Body (Fast & Deterministic)"
        Gateway[Guardrail Gateway]
        Policies[Static Policy Engine]
    end

    subgraph "The Memory (Contextual)"
        Graph[Operation Graph]
        History[(Redis / Neo4j)]
    end

    subgraph "The Mind (Slow & Probabilistic)"
        Firewall[Cognitive Firewall]
        SAE[Sparse Autoencoder]
        Oracle[Bayesian Risk Oracle]
    end

    Gateway -- 1. Check Identity --> Policies
    Gateway -- 2. Fetch Context --> Graph
    Graph -- 3. Risk Signal --> Firewall
    Firewall -- 4. SAE Analysis --> SAE
    SAE -- 5. Hidden Intent --> Oracle
    Oracle -- 6. Posterior Probability --> Gateway
    Gateway -- 7. ALLOW / BLOCK --> Tools[Tool Execution]


1. The Body (Guardrail Gateway)

"The Reflex."

Function: Deterministic, rule-based blocking.

Role: Handles identity verification, rate limiting, and hard bans on dangerous tools (e.g., rm -rf, nmap for unverified users).

Why: We do not waste GPU cycles on obvious threats.

2. The Memory (Operation Graph)

"The Context."

Function: Tracks the sequence of actions over time.

Role: It does not care if you ask to "scan an IP". It cares if you have scanned 50 distinct IPs in the last hour.

Detection: Identifies Kill Chains (Recon $\to$ Exploit $\to$ Exfil).

3. The Mind (Cognitive Firewall)

"The Judgment."

Function: Probabilistic intent analysis using Sparse Autoencoders (SAEs).

Role: It looks inside the model's activation space to detect hidden intents like "Deception", "Roleplay", or "Obfuscation" even if the text looks benign.

Logic: Uses Bayesian updates to combine the Memory's history with the Mind's intuition to form a final risk score.

🛡️ Why We Need You (Contributing)

The attackers (GTG-1002) are adapting. They are using "Personas" to bypass filters and "Slow-roll" tactics to bypass rate limits. We need the open-source community to:

Map the Mind: Help us identify new SAE features that correspond to malicious intent (e.g., "Syccophancy", "Power-Seeking").

Harden the Body: Contribute new deterministic rules for emerging tools (MCP, RCE).

Red Team the System: Use the provided Agent configurations to try and break our defenses.

How to Contribute

Backend: Python/FastAPI. Found in /backend.

Frontend: React/TypeScript. Found in /frontend.

Research: Jupyter Notebooks for SAE analysis. Found in /research.

🧪 Red Teaming with "Jules"

We have provided Agent Directives in the red_team/ directory. You can load these files into an AI Agent (Jules, Cursor, or generic LLM) to simulate attacks against the platform.

The Social Engineer: Tries to trick the "Mind" using psychology.

The Slow-Roll: Tries to trick the "Memory" using patience.

The Obfuscator: Tries to trick the "Body" using encoding.

"Intelligence without guardrails is not a tool; it is a vector."
