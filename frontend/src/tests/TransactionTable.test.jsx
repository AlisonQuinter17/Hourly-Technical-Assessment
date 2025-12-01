import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import TransactionTable from '../components/TransactionTable';

describe('TransactionTable Component', () => {
    it('renders table headers', () => {
        const transactions = [];
        render(<TransactionTable transactions={transactions} />);

        expect(screen.getByText(/ID/i)).toBeInTheDocument();
        expect(screen.getByText(/Created At/i)).toBeInTheDocument();
        expect(screen.getByText(/Status/i)).toBeInTheDocument();
        expect(screen.getByText(/Num Records/i)).toBeInTheDocument();
        expect(screen.getByText(/Total Debit/i)).toBeInTheDocument();
        expect(screen.getByText(/Total Credit/i)).toBeInTheDocument();
    });

    it('shows empty message when no transactions', () => {
        const transactions = [];
        render(<TransactionTable transactions={transactions} />);

        expect(screen.getByText(/No transactions found/i)).toBeInTheDocument();
    });

    it('renders transaction rows', () => {
        const transactions = [
            {
                id: 'test-id-123',
                created_at: '2024-01-01T00:00:00',
                status: 'done',
                num_records: 10,
                total_debit: 100.50,
                total_credit: 200.75,
            },
        ];

        render(<TransactionTable transactions={transactions} />);

        expect(screen.getByText('test-id-123')).toBeInTheDocument();
        expect(screen.getByText('done')).toBeInTheDocument();
        expect(screen.getByText('10')).toBeInTheDocument();
        expect(screen.getByText('$100.50')).toBeInTheDocument();
        expect(screen.getByText('$200.75')).toBeInTheDocument();
    });

    it('applies correct status badge colors', () => {
        const transactions = [
            {
                id: 'test-1',
                created_at: '2024-01-01T00:00:00',
                status: 'done',
                num_records: 5,
                total_debit: 50,
                total_credit: 100,
            },
        ];

        const { container } = render(<TransactionTable transactions={transactions} />);
        const badge = container.querySelector('.bg-green-100');

        expect(badge).toBeInTheDocument();
    });
});
