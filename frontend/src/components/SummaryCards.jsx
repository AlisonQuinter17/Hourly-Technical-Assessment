import React from 'react';

const Card = ({ title, value, color }) => (
  <div className={`bg-white p-6 rounded-lg shadow-md border-l-4 ${color}`}>
    <h3 className="text-gray-500 text-xs font-medium uppercase tracking-wider">{title}</h3>
    <p className="mt-2 text-2xl font-medium text-gray-700">{value}</p>
  </div>
);

const SummaryCards = ({ transactions }) => {
  const totalDebit = transactions.reduce((sum, t) => sum + (t.total_debit || 0), 0);
  const totalCredit = transactions.reduce((sum, t) => sum + (t.total_credit || 0), 0);
  const totalNet = totalCredit - totalDebit;

  const formatCurrency = (val) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <Card title="Total Debit" value={formatCurrency(totalDebit)} color="border-yellow-500" />
      <Card title="Total Credit" value={formatCurrency(totalCredit)} color="border-yellow-500" />
      <Card title="Net Total" value={formatCurrency(totalNet)} color="border-yellow-500" />
    </div>
  );
};

export default SummaryCards;
