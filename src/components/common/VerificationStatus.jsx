import { AlertTriangle, CheckCircle2, Clock, ShieldAlert } from 'lucide-react';
import Badge from '@/components/ui/Badge';
import { cn } from '@/utils/helpers';

const iconMap = {
  verified: CheckCircle2,
  pending: Clock,
  review: AlertTriangle,
  failed: ShieldAlert,
};

function VerificationStatus({ label, value, status = 'pending', compact = false }) {
  const Icon = iconMap[status] || Clock;

  return (
    <div
      className={cn(
        'flex items-center justify-between gap-4 rounded-lg border border-slate-200 bg-white p-4',
        compact && 'p-3',
      )}
    >
      <div className="flex min-w-0 items-center gap-3">
        <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md border border-slate-200 bg-slate-50 text-mutedBlue-700">
          <Icon className="h-5 w-5" />
        </span>
        <div className="min-w-0">
          <p className="truncate text-sm font-medium text-charcoal">{label}</p>
          <p className="mt-1 truncate text-sm text-slate-500">{value}</p>
        </div>
      </div>
      <Badge variant={status}>{status}</Badge>
    </div>
  );
}

export default VerificationStatus;
