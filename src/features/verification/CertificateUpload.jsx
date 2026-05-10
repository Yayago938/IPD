import Card from '@/components/ui/Card';
import FileUpload from '@/components/common/FileUpload';

function CertificateUpload() {
  return (
    <Card>
      <Card.Header>
        <Card.Title>Certificate Upload</Card.Title>
        <p className="mt-2 text-sm text-slate-500">
          Add wipe certificates and detached signature artifacts for frontend verification review.
        </p>
      </Card.Header>
      <Card.Content>
        <FileUpload />
      </Card.Content>
    </Card>
  );
}

export default CertificateUpload;
