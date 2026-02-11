import axios from 'axios';
import { GuardRequest, GuardDecision } from '../types/api.js';

const API_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';

export const checkRequest = async (req: GuardRequest): Promise<GuardDecision> => {
  try {
    const response = await axios.post(`${API_URL}/guard/check`, req);
    return response.data;
  } catch (error) {
    console.error("Backend unreachable, returning mock safety response");
    // Fallback/Mock logic for demo purposes
    return {
      verdict: 'BLOCK',
      risk_score: 1.0,
      reason: 'Backend Error - Default Fail Closed'
    };
  }
};
