import React from 'react';

const TransactionTable = ({ transactions }) => {
  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'created_at', label: 'Created At' },
    { key: 'status', label: 'Status' },
    { key: 'num_records', label: 'Num Records' },
    { key: 'total_debit', label: 'Total Debit' },
    { key: 'total_credit', label: 'Total Credit' },
  ];

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'done':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map(col => (
                <th key={col.key} className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transactions.length === 0 ? (
              <tr>
                <td colSpan="6" className="px-6 py-4 text-center text-gray-500">No transactions found. Please upload a CSV file to get started.</td>
              </tr>
            ) : (
              transactions.map((t) => (
                <tr key={t.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 cursor-default group">
                    <span className="group-hover:hidden">{t.id.slice(0, 8)}...</span>
                    <span className="hidden group-hover:inline">{t.id}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(t.created_at).toISOString().substring(0, 10).replace(/-/g, '-')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadgeClass(t.status)}`}>
                      {t.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{t.num_records}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${t.total_debit?.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${t.total_credit?.toFixed(2)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TransactionTable;
