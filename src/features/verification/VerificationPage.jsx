import CertificateUpload from './CertificateUpload';
import HashVerification from './HashVerification';

function VerificationPage() {
  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <div>
        <p className="text-sm font-medium uppercase tracking-wide text-mutedBlue-700">
          Evidence intake
        </p>
        <h2 className="mt-2 text-2xl font-semibold text-charcoal">Certificate Verification</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
          Upload certificate evidence, enter reported hashes, and review signature validation states
          before approving secure wipe records.
        </p>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <CertificateUpload />
        <HashVerification />
      </div>
    </div>
  );
}

export default VerificationPage;
