import { KeyRound, ServerCog, ShieldCheck, UserRound } from 'lucide-react';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Input from '@/components/ui/Input';

function SettingsPage() {
  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <div>
        <p className="text-sm font-medium uppercase tracking-wide text-mutedBlue-700">
          Workspace controls
        </p>
        <h2 className="mt-2 text-xl font-semibold text-charcoal sm:text-2xl">Settings</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
          Configure profile metadata, security preferences, and placeholder integration details for
          future platform connections.
        </p>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <Card.Header>
            <div className="flex items-center gap-3">
              <UserRound className="h-5 w-5 text-mutedBlue-700" />
              <Card.Title>Profile Settings</Card.Title>
            </div>
          </Card.Header>
          <Card.Content className="space-y-4">
            <Input label="Display name" name="displayName" defaultValue="Security Console" />
            <Input
              label="Organization"
              name="organization"
              defaultValue="Enterprise Compliance Office"
            />
            <Input label="Contact email" name="email" defaultValue="security@example.com" type="email" />
            <Button className="w-full sm:w-auto">Save profile</Button>
          </Card.Content>
        </Card>

        <Card>
          <Card.Header>
            <div className="flex items-center gap-3">
              <ShieldCheck className="h-5 w-5 text-mutedBlue-700" />
              <Card.Title>Security Settings</Card.Title>
            </div>
          </Card.Header>
          <Card.Content className="space-y-4">
            <label className="flex items-center justify-between gap-4 rounded-lg border border-slate-200 p-4">
              <span>
                <span className="block text-sm font-medium text-charcoal">Require manual review</span>
                <span className="mt-1 block text-xs text-slate-500">
                  Flag ambiguous wipe evidence before report export.
                </span>
              </span>
              <input className="h-5 w-5 accent-slate-700" type="checkbox" defaultChecked />
            </label>
            <label className="flex items-center justify-between gap-4 rounded-lg border border-slate-200 p-4">
              <span>
                <span className="block text-sm font-medium text-charcoal">Retain audit trail</span>
                <span className="mt-1 block text-xs text-slate-500">
                  Keep local UI events visible in the reports workspace.
                </span>
              </span>
              <input className="h-5 w-5 accent-slate-700" type="checkbox" defaultChecked />
            </label>
            <Button className="w-full sm:w-auto" variant="secondary">
              <KeyRound className="h-4 w-4" />
              Rotate local token placeholder
            </Button>
          </Card.Content>
        </Card>

        <Card className="xl:col-span-2">
          <Card.Header>
            <div className="flex items-center gap-3">
              <ServerCog className="h-5 w-5 text-mutedBlue-700" />
              <Card.Title>API Placeholder</Card.Title>
            </div>
            <p className="mt-2 text-sm text-slate-500">
              Frontend-only configuration fields reserved for a future secure verification service.
            </p>
          </Card.Header>
          <Card.Content className="grid gap-4 md:grid-cols-3">
            <Input label="Endpoint URL" name="endpoint" placeholder="https://verification.example.com" />
            <Input label="Tenant ID" name="tenant" placeholder="tenant-securewipe" />
            <Input label="Evidence retention days" name="retention" defaultValue="365" type="number" />
          </Card.Content>
        </Card>
      </div>
    </div>
  );
}

export default SettingsPage;
