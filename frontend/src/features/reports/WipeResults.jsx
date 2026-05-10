import { Download, FileBadge2 } from 'lucide-react';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import { wipeResults } from '@/features/dashboard/dashboardData';

function WipeResults() {
  return (
    <div className="grid gap-4 lg:grid-cols-3">
      {wipeResults.map((result) => (
        <Card key={result.asset}>
          <Card.Content>
            <div className="flex items-start justify-between gap-4">
              <span className="flex h-10 w-10 items-center justify-center rounded-md border border-slate-200 bg-slate-50 text-mutedBlue-700">
                <FileBadge2 className="h-5 w-5" />
              </span>
              <Badge variant={result.status}>{result.certificate}</Badge>
            </div>
            <h3 className="mt-5 text-base font-semibold text-charcoal">{result.asset}</h3>
            <dl className="mt-5 space-y-3 text-sm">
              <div className="flex justify-between gap-4">
                <dt className="text-slate-500">Serials</dt>
                <dd className="font-medium text-charcoal">{result.serials}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-slate-500">Method</dt>
                <dd className="text-right font-medium text-charcoal">{result.method}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-slate-500">Completion</dt>
                <dd className="font-medium text-charcoal">{result.completion}</dd>
              </div>
            </dl>
            <Button className="mt-6 w-full" variant="secondary">
              <Download className="h-4 w-4" />
              Export result
            </Button>
          </Card.Content>
        </Card>
      ))}
    </div>
  );
}

export default WipeResults;
