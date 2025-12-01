import React, { useRef, useState } from 'react';
import { IoCloudUploadOutline } from "react-icons/io5";
import api from '../api';

const FileUpload = ({ onUploadSuccess }) => {
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setError(null);

    try {
      const response = await api.post('/transactions/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onUploadSuccess(response.data);
      e.target.value = '';
    } catch (err) {
      console.error(err);
      setError("Failed to upload file. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex items-center justify-end gap-2 w-full">
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="hidden"
      />
      <button
        onClick={handleButtonClick}
        disabled={uploading}
        className={`px-4 py-2 rounded-md text-white font-medium transition-colors cursor-pointer flex items-center gap-2 ${uploading
          ? 'bg-gray-400 cursor-not-allowed'
          : 'bg-yellow-600 hover:bg-yellow-700'
          }`}
      >
        {!uploading && <IoCloudUploadOutline size={22} />}
        {uploading ? 'Uploading...' : 'Upload CSV File'}
      </button>
      {error && <p className="text-red-600 text-sm">{error}</p>}
    </div>
  );
};

export default FileUpload;
