const test = require('node:test');
const assert = require('node:assert');
const { computeGaps } = require('./gaps');

const now = new Date('2026-10-05T10:40:00Z');
const ago = (min) => new Date(now.getTime() - min * 60000).toISOString();

test('flags unowned open requests, ignores done ones', () => {
  const g = computeGaps(
    [{ id: 'c1', student: 'Riya', requests: [
      { id: 'r1', type: 'hostel notice', department: '', status: 'new', updatedAt: ago(1) },
      { id: 'r2', type: 'fee extension', department: null, status: 'done', updatedAt: ago(1) },
    ] }],
    { now },
  );
  assert.deepStrictEqual(g.unowned.map((x) => x.requestId), ['r1']);
});

test('flags stuck requests past the limit, oldest first, skips done', () => {
  const g = computeGaps(
    [{ id: 'c1', student: 'A', requests: [
      { id: 'r1', type: 't', department: 'Accounts', status: 'routed', updatedAt: ago(6) },
      { id: 'r2', type: 't', department: 'Hostel', status: 'in progress', updatedAt: ago(20) },
      { id: 'r3', type: 't', department: 'Library', status: 'routed', updatedAt: ago(1) },
      { id: 'r4', type: 't', department: 'Library', status: 'done', updatedAt: ago(99) },
    ] }],
    { now, stuckAfterMinutes: 5 },
  );
  assert.deepStrictEqual(g.stuck.map((x) => x.requestId), ['r2', 'r1']);
});

test('flags students open in 3+ departments (distinct, open only)', () => {
  const mk = (id, dept, status = 'routed') => ({ id, type: 't', department: dept, status, updatedAt: ago(1) });
  const g = computeGaps(
    [
      { id: 'c1', student: 'Riya', requests: [mk('a', 'Accounts'), mk('b', 'Exam Cell'), mk('c', 'Counselling')] },
      { id: 'c2', student: 'Two', requests: [mk('d', 'Accounts'), mk('e', 'Accounts'), mk('f', 'Hostel')] },
      { id: 'c3', student: 'DoneOne', requests: [mk('g', 'Accounts'), mk('h', 'Hostel'), mk('i', 'Library', 'done')] },
    ],
    { now },
  );
  assert.deepStrictEqual(g.multiDepartment.map((x) => x.caseId), ['c1']);
  assert.strictEqual(g.multiDepartment[0].departmentCount, 3);
});

test('bad timestamp is surfaced as stuck, empty input is safe', () => {
  const g = computeGaps(
    [{ id: 'c1', student: 'X', requests: [{ id: 'r', type: 't', department: 'Hostel', status: 'new', updatedAt: 'nope' }] }],
    { now },
  );
  assert.strictEqual(g.counts.stuck, 1);
  assert.deepStrictEqual(computeGaps([], { now }).counts, { unowned: 0, stuck: 0, multiDepartment: 0 });
});
