"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";

const API_BASE = "http://localhost:8000/api"

interface Transaction {
  id: number;
  address: string;
  tx_hash: string;
}

export default function AddressPage({ params }: { params: Promise<{ address: string }> }) {
  const { address } = use(params);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);

  const fetchTransactions = async () => {
    const res = await fetch(`${API_BASE}/addresses/${address}/transactions/?page=${page}`);
    const data = await res.json();
    setTransactions(data["results"]);
    setHasNext(!!data.next);
  };

  useEffect(() => {
    fetchTransactions();
  }, [page]);

  return (
    <main className="p-6 max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <Link 
          href="/" 
          className="flex items-center text-blue-500 hover:underline"
        >
          Back
        </Link>
      </div>
      <h1 className="text-2xl font-bold mb-4">{address}</h1>

      <ul className="space-y-2 mb-4">
        {transactions.map((tx) => (
          <li key={tx.id} className="border p-2 rounded font-mono">
            {tx.tx_hash}
          </li>
        ))}
      </ul>

      <div className="flex justify-between">
        <button
          disabled={page <= 1}
          onClick={() => setPage(page - 1)}
          className="px-3 py-1 border rounded disabled:opacity-50"
        >
          Prev
        </button>
        <button
          disabled={!hasNext}
          onClick={() => setPage(page + 1)}
          className="px-3 py-1 border rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </main>
  );
}
