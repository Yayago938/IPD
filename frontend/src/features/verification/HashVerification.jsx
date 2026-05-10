import { Fingerprint, ShieldCheck } from 'lucide-react';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Input from '@/components/ui/Input';
import VerificationStatus from '@/components/common/VerificationStatus';

function HashVerification() {
  return (
    <Card>
      <Card.Header>
        <Card.Title>Hash and Signature Verification</Card.Title>
        <p className="mt-2 text-sm text-slate-500">
          Enter a reported SHA-256 hash to compare against the uploaded certificate record.
        </p>
      </Card.Header>
      <Card.Content className="space-y-5">
        <Input
          label="Certificate hash"
          name="hash"
          placeholder="e3b0c44298fc1c149afbf4c8996fb924..."
          hint="Mock validation only. No cryptographic verification is performed."
        />
        <div className="flex flex-col gap-3 sm:flex-row">
          <Button className="w-full sm:w-auto">
            <ShieldCheck className="h-4 w-4" />
            Verify signature
          </Button>
          <Button className="w-full sm:w-auto" variant="secondary">
            <Fingerprint className="h-4 w-4" />
            Compare hash
          </Button>
        </div>
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
          <p className="text-sm font-semibold text-charcoal">Signature result panel</p>
          <div className="mt-4 space-y-3">
            <VerificationStatus
              label="Certificate issuer"
              value="SecureWipe Authority CA"
              status="verified"
            />
            <VerificationStatus
              label="Detached signature"
              value="Awaiting uploaded signature"
              status="pending"
            />
            <VerificationStatus label="Hash comparison" value="Ready for review" status="review" />
          </div>
        </div>
      </Card.Content>
    </Card>
  );
}

export default HashVerification;
