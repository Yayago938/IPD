import { cn } from '@/utils/helpers';

const variants = {
  verified: 'border-emerald-200 bg-emerald-50 text-emerald-700',
  pending: 'border-slate-200 bg-slate-50 text-slate-600',
  review: 'border-amber-200 bg-amber-50 text-amber-700',
  failed: 'border-red-200 bg-red-50 text-red-700',
  info: 'border-mutedBlue-100 bg-mutedBlue-50 text-mutedBlue-700',
};

function Badge({ children, variant = 'info', className = '' }) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium',
        variants[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}

export default Badge;
