import { Activity, DatabaseZap, FileCheck2, ShieldCheck } from 'lucide-react';
import Badge from '@/components/ui/Badge';
import Card from '@/components/ui/Card';
import VerificationStatus from '@/components/common/VerificationStatus';
import { formatDate, formatNumber } from '@/utils/helpers';
import { recentWipeJobs, summaryCards, verificationWidgets } from './dashboardData';

const summaryIcons = [ShieldCheck, DatabaseZap, Activity, FileCheck2];

function DashboardPage() {
  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <div>
        <p className="text-sm font-medium uppercase tracking-wide text-mutedBlue-700">
          Compliance overview
        </p>
        <h2 className="mt-2 text-2xl font-semibold text-charcoal">Wipe Verification Dashboard</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
          Review certificate integrity, wipe completion evidence, and audit readiness across secure
          deletion workflows.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {summaryCards.map((card, index) => {
          const Icon = summaryIcons[index];
          return (
            <Card key={card.label}>
              <Card.Content>
                <div className="flex items-start justify-between gap-3">
                  <span className="flex h-11 w-11 items-center justify-center rounded-md border border-slate-200 bg-slate-50 text-mutedBlue-700">
                    <Icon className="h-5 w-5" />
                  </span>
                  <Badge variant={card.status}>{card.change}</Badge>
                </div>
                <p className="mt-5 text-sm text-slate-500">{card.label}</p>
                <p className="mt-2 text-3xl font-semibold text-charcoal">
                  {formatNumber(card.value)}
                </p>
              </Card.Content>
            </Card>
          );
        })}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.35fr_0.85fr]">
        <Card>
          <Card.Header>
            <Card.Title>Recent Wipe Jobs</Card.Title>
          </Card.Header>
          <Card.Content className="p-0">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-100 text-left text-sm">
                <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                  <tr>
                    <th className="px-6 py-3 font-semibold">Job</th>
                    <th className="px-6 py-3 font-semibold">Asset Group</th>
                    <th className="px-6 py-3 font-semibold">Method</th>
                    <th className="px-6 py-3 font-semibold">Date</th>
                    <th className="px-6 py-3 font-semibold">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {recentWipeJobs.map((job) => (
                    <tr key={job.id} className="hover:bg-slate-50">
                      <td className="px-6 py-4">
                        <p className="font-medium text-charcoal">{job.id}</p>
                        <p className="mt-1 text-xs text-slate-500">{job.certificate}</p>
                      </td>
                      <td className="min-w-56 px-6 py-4 text-slate-600">{job.asset}</td>
                      <td className="whitespace-nowrap px-6 py-4 text-slate-600">{job.method}</td>
                      <td className="whitespace-nowrap px-6 py-4 text-slate-600">
                        {formatDate(job.date)}
                      </td>
                      <td className="whitespace-nowrap px-6 py-4">
                        <Badge variant={job.status}>{job.status}</Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card.Content>
        </Card>

        <Card>
          <Card.Header>
            <Card.Title>Verification Status</Card.Title>
          </Card.Header>
          <Card.Content className="space-y-3">
            {verificationWidgets.map((widget) => (
              <VerificationStatus key={widget.label} {...widget} compact />
            ))}
          </Card.Content>
        </Card>
      </div>
    </div>
  );
}

export default DashboardPage;
