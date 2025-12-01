import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import SummaryCards from '../components/SummaryCards';

describe('SummaryCards Component', () => {
    it('renders all three cards', () => {
        const transactions = [];
        render(<SummaryCards transactions={transactions} />);

        expect(screen.getByText(/Total Debit/i)).toBeInTheDocument();
        expect(screen.getByText(/Total Credit/i)).toBeInTheDocument();
        expect(screen.getByText(/Net Total/i)).toBeInTheDocument();
    });

    it('calculates totals correctly', () => {
        const transactions = [
            { total_debit: 100, total_credit: 200 },
            { total_debit: 50, total_credit: 75 },
        ];

        render(<SummaryCards transactions={transactions} />);

        // Total debit should be 150
        // Total credit should be 275
        // Net total should be 125 (275 - 150)
        expect(screen.getByText('$150.00')).toBeInTheDocument();
        expect(screen.getByText('$275.00')).toBeInTheDocument();
        expect(screen.getByText('$125.00')).toBeInTheDocument();
    });

    it('handles empty transactions', () => {
        const transactions = [];
        render(<SummaryCards transactions={transactions} />);
        const zeroValues = screen.getAllByText('$0.00');
        expect(zeroValues).toHaveLength(3);
    });
});
