import { Download, FileSpreadsheet, Printer } from 'lucide-react';
import AuditTable from '@/components/common/AuditTable';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import { auditLogs } from '@/features/dashboard/dashboardData';
import WipeResults from './WipeResults';

function ReportsPage() {
  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <div className="flex flex-col justify-between gap-4 xl:flex-row xl:items-end">
        <div>
          <p className="text-sm font-medium uppercase tracking-wide text-mutedBlue-700">
            Audit evidence
          </p>
          <h2 className="mt-2 text-xl font-semibold text-charcoal sm:text-2xl">
            Reports and Wipe Results
          </h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            Review wipe result summaries, export evidence bundles, and inspect recent audit events.
          </p>
        </div>
        <div className="flex w-full flex-col gap-3 sm:flex-row sm:flex-wrap xl:w-auto">
          <Button className="w-full sm:w-auto" variant="secondary">
            <FileSpreadsheet className="h-4 w-4" />
            Export CSV
          </Button>
          <Button className="w-full sm:w-auto" variant="secondary">
            <Printer className="h-4 w-4" />
            Print report
          </Button>
          <Button className="w-full sm:w-auto">
            <Download className="h-4 w-4" />
            Export bundle
          </Button>
        </div>
      </div>

      <WipeResults />

      <Card>
        <Card.Header>
          <Card.Title>Audit Log</Card.Title>
          <p className="mt-2 text-sm text-slate-500">
            Immutable-style frontend record of review activity and verification outcomes.
          </p>
        </Card.Header>
        <Card.Content>
          <AuditTable logs={auditLogs} />
        </Card.Content>
      </Card>
    </div>
  );
}

export default ReportsPage;
