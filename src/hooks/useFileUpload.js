import { useCallback, useState } from 'react';

export function useFileUpload() {
  const [files, setFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);

  const addFiles = useCallback((fileList) => {
    const nextFiles = Array.from(fileList || []);
    if (nextFiles.length) {
      setFiles(nextFiles);
    }
  }, []);

  const removeFile = useCallback((fileName) => {
    setFiles((currentFiles) => currentFiles.filter((file) => file.name !== fileName));
  }, []);

  const clearFiles = useCallback(() => setFiles([]), []);

  const dragHandlers = {
    onDragEnter: (event) => {
      event.preventDefault();
      setIsDragging(true);
    },
    onDragOver: (event) => {
      event.preventDefault();
      setIsDragging(true);
    },
    onDragLeave: (event) => {
      event.preventDefault();
      setIsDragging(false);
    },
    onDrop: (event) => {
      event.preventDefault();
      setIsDragging(false);
      addFiles(event.dataTransfer.files);
    },
  };

  return {
    files,
    isDragging,
    addFiles,
    removeFile,
    clearFiles,
    dragHandlers,
  };
}
