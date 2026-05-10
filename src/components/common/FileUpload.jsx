import { FileCheck2, Upload, X } from 'lucide-react';
import Button from '@/components/ui/Button';
import { useFileUpload } from '@/hooks/useFileUpload';
import { cn, formatBytes } from '@/utils/helpers';

function FileUpload({ onFilesChange }) {
  const { files, isDragging, addFiles, removeFile, dragHandlers } = useFileUpload();

  const handleChange = (event) => {
    addFiles(event.target.files);
    onFilesChange?.(Array.from(event.target.files || []));
  };

  return (
    <div className="space-y-4">
      <label
        className={cn(
          'flex min-h-44 cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed bg-white px-4 py-8 text-center transition-colors sm:min-h-56 sm:px-6 sm:py-10',
          isDragging
            ? 'border-mutedBlue-500 bg-mutedBlue-50'
            : 'border-slate-300 hover:border-mutedBlue-500 hover:bg-slate-50',
        )}
        {...dragHandlers}
      >
        <input
          className="sr-only"
          type="file"
          accept=".pdf,.pem,.crt,.cer,.sig,.json"
          onChange={handleChange}
        />
        <span className="flex h-12 w-12 items-center justify-center rounded-md border border-slate-200 bg-slate-50 text-mutedBlue-700">
          <Upload className="h-5 w-5" />
        </span>
        <span className="mt-4 text-base font-semibold text-charcoal">
          Drag certificate files here
        </span>
        <span className="mt-2 max-w-md text-sm text-slate-500">
          Upload signed certificates, PEM chains, detached signatures, or verification manifests.
        </span>
        <span className="mt-5">
          <Button as="span" variant="secondary">
            Browse files
          </Button>
        </span>
      </label>

      {files.length ? (
        <div className="space-y-3">
          {files.map((file) => (
            <div
              key={`${file.name}-${file.size}`}
              className="flex items-center justify-between gap-3 rounded-lg border border-slate-200 bg-white p-3 sm:gap-4 sm:p-4"
            >
              <div className="flex min-w-0 items-center gap-3">
                <FileCheck2 className="h-5 w-5 shrink-0 text-mutedBlue-700" />
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-charcoal">{file.name}</p>
                  <p className="mt-1 text-xs text-slate-500">{formatBytes(file.size)}</p>
                </div>
              </div>
              <Button
                aria-label={`Remove ${file.name}`}
                size="icon"
                variant="ghost"
                onClick={() => removeFile(file.name)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}

export default FileUpload;
