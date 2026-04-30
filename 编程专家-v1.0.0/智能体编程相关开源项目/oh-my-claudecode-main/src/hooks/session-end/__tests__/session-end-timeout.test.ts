import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';

// ── hooks.json timeout validation ──────────────────────────────────────────

describe('SessionEnd hook timeout (issue #1700)', () => {
  it('hooks.json SessionEnd timeout is at least 30 seconds', () => {
    // Read from the repository root hooks.json
    const hooksJsonPath = path.resolve(__dirname, '../../../../hooks/hooks.json');
    const hooksJson = JSON.parse(fs.readFileSync(hooksJsonPath, 'utf-8'));

    const sessionEndEntries = hooksJson.hooks.SessionEnd;
    expect(sessionEndEntries).toBeDefined();
    expect(Array.isArray(sessionEndEntries)).toBe(true);

    for (const entry of sessionEndEntries) {
      for (const hook of entry.hooks) {
        expect(hook.timeout).toBeGreaterThanOrEqual(30);
      }
    }
  });
});

// ── fire-and-forget notification behavior ──────────────────────────────────

vi.mock('../callbacks.js', () => ({
  triggerStopCallbacks: vi.fn(async () => {
    // Simulate a slow notification (2s) — should not block session end
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }),
}));

vi.mock('../../../notifications/index.js', () => ({
  notify: vi.fn(async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }),
}));

vi.mock('../../../features/auto-update.js', () => ({
  getOMCConfig: vi.fn(() => ({})),
}));

vi.mock('../../../notifications/config.js', () => ({
  buildConfigFromEnv: vi.fn(() => null),
  getEnabledPlatforms: vi.fn(() => []),
  getNotificationConfig: vi.fn(() => null),
}));

vi.mock('../../../tools/python-repl/bridge-manager.js', () => ({
  cleanupBridgeSessions: vi.fn(async () => ({
    requestedSessions: 0,
    foundSessions: 0,
    terminatedSessions: 0,
    errors: [],
  })),
}));

vi.mock('../../../openclaw/index.js', () => ({
  wakeOpenClaw: vi.fn().mockResolvedValue({ gateway: 'test', success: true }),
}));

import { processSessionEnd } from '../index.js';
import { triggerStopCallbacks } from '../callbacks.js';

describe('SessionEnd fire-and-forget notifications (issue #1700)', () => {
  let tmpDir: string;
  let transcriptPath: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'omc-session-end-timeout-'));
    transcriptPath = path.join(tmpDir, 'transcript.jsonl');
    fs.writeFileSync(
      transcriptPath,
      JSON.stringify({
        type: 'assistant',
        message: { content: [{ type: 'text', text: 'done' }] },
      }),
      'utf-8',
    );
    vi.clearAllMocks();
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
    vi.restoreAllMocks();
  });

  it('processSessionEnd completes well before slow notifications finish', async () => {
    const start = Date.now();

    await processSessionEnd({
      session_id: 'timeout-test-1',
      transcript_path: transcriptPath,
      cwd: tmpDir,
      permission_mode: 'default',
      hook_event_name: 'SessionEnd',
      reason: 'clear',
    });

    const elapsed = Date.now() - start;

    // triggerStopCallbacks was called (fire-and-forget)
    expect(triggerStopCallbacks).toHaveBeenCalled();

    // The function should complete in well under the 2s mock delay.
    // With fire-and-forget, it races with a 5s cap, but the synchronous
    // work should be fast. We give generous margin but ensure it's not
    // waiting the full 2s for the mock notification to resolve.
    // In practice this finishes in <100ms; 1500ms is a safe CI threshold.
    expect(elapsed).toBeLessThan(1500);
  });
});
