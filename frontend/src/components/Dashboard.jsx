import React, { useState, useEffect } from 'react';
import SummaryCards from './SummaryCards';
import TransactionTable from './TransactionTable';
import api from '../api';
import FileUpload from './FileUpload';

const Dashboard = () => {
  const [transactions, setTransactions] = useState([]);

  const fetchTransactions = async () => {
    try {
      const response = await api.get('/transactions');
      const sorted = response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      setTransactions(sorted);
    } catch (error) {
      console.error("Error fetching transactions:", error);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  useEffect(() => {
    const hasProcessing = transactions.some(t => t.status === 'processing' || t.status === 'pending');

    let interval;
    if (hasProcessing) {
      interval = setInterval(fetchTransactions, 2000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [transactions]);

  const handleUploadSuccess = (newTransaction) => {
    setTransactions(prev => [newTransaction, ...prev]);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-10 flex items-center justify-between">
          <h1 className="text-3xl font-semibold text-gray-700">Transactions</h1>
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </header>

        <main>
          <SummaryCards transactions={transactions} />
          <TransactionTable transactions={transactions} />
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
