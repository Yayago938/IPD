export const summaryCards = [
  { label: 'Verified Certificates', value: 1284, change: '+8.2%', status: 'verified' },
  { label: 'Wipe Jobs Reviewed', value: 412, change: '+3.1%', status: 'info' },
  { label: 'Pending Review', value: 18, change: '-4.4%', status: 'review' },
  { label: 'Failed Validation', value: 6, change: '+1.0%', status: 'failed' },
];

export const recentWipeJobs = [
  {
    id: 'SWP-98241',
    asset: 'Finance Workstation Batch A',
    certificate: 'cert-fw-a-2026-05-08.pdf',
    method: 'NIST 800-88 Clear',
    status: 'verified',
    date: '2026-05-08',
  },
  {
    id: 'SWP-98233',
    asset: 'Legal Archive SSD Pool',
    certificate: 'legal-ssd-pool.sig',
    method: 'DoD 5220.22-M',
    status: 'review',
    date: '2026-05-07',
  },
  {
    id: 'SWP-98209',
    asset: 'HR Laptop Return Queue',
    certificate: 'hr-return-queue.pdf',
    method: 'Cryptographic Erase',
    status: 'verified',
    date: '2026-05-06',
  },
  {
    id: 'SWP-98192',
    asset: 'Decommissioned Server Rack 12',
    certificate: 'rack-12-chain.pem',
    method: 'NIST 800-88 Purge',
    status: 'failed',
    date: '2026-05-05',
  },
];

export const verificationWidgets = [
  { label: 'Certificate Chain', value: 'Valid', status: 'verified' },
  { label: 'Issuer Signature', value: 'Matched', status: 'verified' },
  { label: 'Hash Integrity', value: 'Pending', status: 'pending' },
  { label: 'Policy Mapping', value: 'Manual Review', status: 'review' },
];

export const auditLogs = [
  {
    id: 'AUD-7719',
    actor: 'Compliance Analyst',
    action: 'Verified certificate chain',
    target: 'SWP-98241',
    timestamp: '2026-05-08 14:21',
    outcome: 'verified',
  },
  {
    id: 'AUD-7711',
    actor: 'Security Officer',
    action: 'Exported wipe report',
    target: 'SWP-98209',
    timestamp: '2026-05-07 10:44',
    outcome: 'verified',
  },
  {
    id: 'AUD-7702',
    actor: 'Audit Reviewer',
    action: 'Flagged signature mismatch',
    target: 'SWP-98192',
    timestamp: '2026-05-06 16:09',
    outcome: 'failed',
  },
  {
    id: 'AUD-7695',
    actor: 'Compliance Analyst',
    action: 'Queued policy exception review',
    target: 'SWP-98233',
    timestamp: '2026-05-06 09:32',
    outcome: 'review',
  },
];

export const wipeResults = [
  {
    asset: 'Finance Workstation Batch A',
    serials: 42,
    method: 'NIST 800-88 Clear',
    completion: '100%',
    certificate: 'Verified',
    status: 'verified',
  },
  {
    asset: 'Legal Archive SSD Pool',
    serials: 16,
    method: 'DoD 5220.22-M',
    completion: '98%',
    certificate: 'Review Needed',
    status: 'review',
  },
  {
    asset: 'Decommissioned Server Rack 12',
    serials: 11,
    method: 'NIST 800-88 Purge',
    completion: '91%',
    certificate: 'Signature Failed',
    status: 'failed',
  },
];
