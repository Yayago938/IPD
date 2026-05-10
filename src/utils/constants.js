export const APP_NAME = 'SecureWipe Verification Portal';

export const NAV_ITEMS = [
  { label: 'Dashboard', shortLabel: 'Dashboard', path: '/dashboard', icon: 'LayoutDashboard' },
  { label: 'Verification', shortLabel: 'Verify', path: '/verification', icon: 'ShieldCheck' },
  { label: 'Reports', path: '/reports', icon: 'FileText' },
  { label: 'Settings', path: '/settings', icon: 'Settings' },
];

export const STATUS_VARIANTS = {
  verified: 'verified',
  pending: 'pending',
  review: 'review',
  failed: 'failed',
};
