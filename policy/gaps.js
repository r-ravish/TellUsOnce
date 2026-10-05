// Gaps logic (F10). Pure functions: no I/O, no AI, no decline path.
// Finds three kinds of gaps across cases:
//   1. unowned requests            (open request with no owning department)
//   2. stuck requests              (open request not updated for too long)
//   3. students open in 3+ departments
// For the demo, MINUTES stand in for days (see DEFAULTS.stuckAfterMinutes).

const DEFAULTS = {
  stuckAfterMinutes: 5, // demo: 5 minutes ~ "too many days"
  multiDeptThreshold: 3,
};

// "done" is the only closed status. Everything else counts as open.
const CLOSED_STATUSES = new Set(['done']);

function isOpen(request) {
  return !CLOSED_STATUSES.has(request.status);
}

function hasOwner(request) {
  return typeof request.department === 'string' && request.department.trim() !== '';
}

function minutesSince(timestamp, now) {
  const t = new Date(timestamp).getTime();
  if (Number.isNaN(t)) return Infinity; // unreadable timestamp: treat as stale, never hide it
  return (now.getTime() - t) / 60000;
}

/**
 * @param {Array} cases  [{ id, student, requests: [{ id, type, department, status, updatedAt }] }]
 * @param {Object} [opts] { now, stuckAfterMinutes, multiDeptThreshold }
 * @returns {{ unowned: Array, stuck: Array, multiDepartment: Array, counts: Object }}
 */
function computeGaps(cases, opts = {}) {
  const now = opts.now ? new Date(opts.now) : new Date();
  const stuckAfter = opts.stuckAfterMinutes ?? DEFAULTS.stuckAfterMinutes;
  const multiThreshold = opts.multiDeptThreshold ?? DEFAULTS.multiDeptThreshold;

  const unowned = [];
  const stuck = [];
  const multiDepartment = [];

  for (const c of cases || []) {
    const openDepartments = new Set();

    for (const r of c.requests || []) {
      if (!isOpen(r)) continue;

      const base = {
        caseId: c.id,
        student: c.student,
        requestId: r.id,
        type: r.type,
        department: r.department || null,
        status: r.status,
        updatedAt: r.updatedAt,
      };

      if (!hasOwner(r)) {
        unowned.push({ ...base, reason: 'No department owns this request.' });
      } else {
        openDepartments.add(r.department);
      }

      const idle = minutesSince(r.updatedAt, now);
      if (idle >= stuckAfter) {
        stuck.push({
          ...base,
          idleMinutes: Number.isFinite(idle) ? Math.floor(idle) : null,
          reason: `No update for ${Number.isFinite(idle) ? Math.floor(idle) : 'unknown'} min (limit ${stuckAfter}).`,
        });
      }
    }

    if (openDepartments.size >= multiThreshold) {
      multiDepartment.push({
        caseId: c.id,
        student: c.student,
        departments: [...openDepartments].sort(),
        departmentCount: openDepartments.size,
        reason: `Open in ${openDepartments.size} departments.`,
      });
    }
  }

  // Oldest first so the panel shows the worst items on top.
  stuck.sort((a, b) => (b.idleMinutes ?? Infinity) - (a.idleMinutes ?? Infinity));

  return {
    unowned,
    stuck,
    multiDepartment,
    counts: {
      unowned: unowned.length,
      stuck: stuck.length,
      multiDepartment: multiDepartment.length,
    },
  };
}

module.exports = { computeGaps, DEFAULTS, isOpen, hasOwner };
