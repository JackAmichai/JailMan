export type ActionType = 'recon' | 'exploit' | 'exfiltration' | 'benign';
export type Verdict = 'ALLOW' | 'BLOCK' | 'FLAG';

export interface ToolRequest {
  tool_name: string;
  target: string;
  params: Record<string, any>;
}

export interface GuardRequest {
  request_id: string;
  user_id: string;
  session_id: string;
  prompt: string;
  tool_request?: ToolRequest;
}

export interface GuardDecision {
  verdict: Verdict;
  risk_score: number;
  reason: string;
  // Metadata for visualization:
  sae_features?: Record<string, number>; // What the Mind saw
  graph_risk?: number;                   // What the Memory saw
}
