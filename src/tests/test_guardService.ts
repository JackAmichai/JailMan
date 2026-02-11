import nock from 'nock';
import { checkRequest } from '../api/guardService.js';
import { GuardRequest, GuardDecision } from '../types/api.js';

const mockRequest: GuardRequest = {
  request_id: '123',
  user_id: 'user1',
  session_id: 'session1',
  prompt: 'Hello world',
};

const mockResponse: GuardDecision = {
  verdict: 'ALLOW',
  risk_score: 0.1,
  reason: 'Safe',
};

async function runTests() {
  console.log('Running tests...');

  // Test 1: Successful response
  nock('http://localhost:8000')
    .post('/guard/check')
    .reply(200, mockResponse);

  try {
    const decision = await checkRequest(mockRequest);
    if (decision.verdict === 'ALLOW') {
      console.log('Test 1 Passed: Successfully received ALLOW verdict.');
    } else {
      console.error('Test 1 Failed: Expected ALLOW verdict, got', decision.verdict);
      process.exit(1);
    }
  } catch (error) {
    console.error('Test 1 Failed with error:', error);
    process.exit(1);
  }

  // Test 2: Backend offline (fallback)
  nock.cleanAll();

  // Verify that checkRequest handles errors gracefully (mocking network error)
  nock('http://localhost:8000')
    .post('/guard/check')
    .replyWithError('Network error');

  try {
    const decision = await checkRequest(mockRequest);
    if (decision.verdict === 'BLOCK' && decision.reason.includes('Backend Error')) {
      console.log('Test 2 Passed: Successfully fell back to BLOCK on error.');
    } else {
      console.error('Test 2 Failed: Expected BLOCK verdict and Backend Error reason, got', decision);
      process.exit(1);
    }
  } catch (error) {
    console.error('Test 2 Failed: checkRequest should not throw, but handle error internally.', error);
    process.exit(1);
  }

  console.log('All tests passed!');
}

runTests();
