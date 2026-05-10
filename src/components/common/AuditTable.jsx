import Badge from '@/components/ui/Badge';

function AuditTable({ logs }) {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-5 py-3 font-semibold">Event ID</th>
              <th className="px-5 py-3 font-semibold">Actor</th>
              <th className="px-5 py-3 font-semibold">Action</th>
              <th className="px-5 py-3 font-semibold">Target</th>
              <th className="px-5 py-3 font-semibold">Timestamp</th>
              <th className="px-5 py-3 font-semibold">Outcome</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {logs.map((log) => (
              <tr key={log.id} className="hover:bg-slate-50">
                <td className="whitespace-nowrap px-5 py-4 font-medium text-charcoal">{log.id}</td>
                <td className="whitespace-nowrap px-5 py-4 text-slate-600">{log.actor}</td>
                <td className="min-w-64 px-5 py-4 text-slate-600">{log.action}</td>
                <td className="whitespace-nowrap px-5 py-4 text-slate-600">{log.target}</td>
                <td className="whitespace-nowrap px-5 py-4 text-slate-600">{log.timestamp}</td>
                <td className="whitespace-nowrap px-5 py-4">
                  <Badge variant={log.outcome}>{log.outcome}</Badge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AuditTable;
