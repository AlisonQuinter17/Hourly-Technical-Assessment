import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import FileUpload from '../components/FileUpload';
import api from '../api';

vi.mock('../api');

describe('FileUpload Component', () => {
    it('renders upload button', () => {
        const mockOnUploadSuccess = vi.fn();
        render(<FileUpload onUploadSuccess={mockOnUploadSuccess} />);

        expect(screen.getByText(/Upload CSV File/i)).toBeInTheDocument();
    });

    it('handles file upload successfully', async () => {
        const mockOnUploadSuccess = vi.fn();
        const mockResponse = { data: { id: '123', status: 'pending' } };
        api.post.mockResolvedValue(mockResponse);

        render(<FileUpload onUploadSuccess={mockOnUploadSuccess} />);

        const file = new File(['test'], 'test.csv', { type: 'text/csv' });
        const input = document.querySelector('input[type="file"]');

        fireEvent.change(input, { target: { files: [file] } });

        await waitFor(() => {
            expect(mockOnUploadSuccess).toHaveBeenCalledWith(mockResponse.data);
        });
    });

    it('shows error message on upload failure', async () => {
        const mockOnUploadSuccess = vi.fn();
        api.post.mockRejectedValue(new Error('Upload failed'));

        render(<FileUpload onUploadSuccess={mockOnUploadSuccess} />);

        const file = new File(['test'], 'test.csv', { type: 'text/csv' });
        const input = document.querySelector('input[type="file"]');

        fireEvent.change(input, { target: { files: [file] } });

        await waitFor(() => {
            expect(screen.getByText(/Failed to upload file/i)).toBeInTheDocument();
        });
    });
});
