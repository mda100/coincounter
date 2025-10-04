"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

const API_BASE = "http://localhost:8000/api"

interface Address {
  id: number;
  address: string;
  final_balance: number;
}

export default function Home() {

  // state
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [newAddress, setNewAddress] = useState("");
  const router = useRouter();

  // methods
  const fetchAddresses = async () => {
    console.log('Fetching from:', `${API_BASE}/addresses/`);
    const res = await fetch(`${API_BASE}/addresses/`);
    const data = await res.json();
    setAddresses(data["results"]);
  };

  const addAddress = async () => {
    await fetch(`${API_BASE}/addresses/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ address: newAddress }),
    });
    setNewAddress("");
    fetchAddresses();
  };

  const deleteAddress = async (address: string) => {
    await fetch(`${API_BASE}/addresses/${address}/`, { method: "DELETE" });
    fetchAddresses();
  };

  useEffect(() => {
    fetchAddresses();
  }, []);


  // html
  return (
    <main className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Addresses</h1>

      <div className="flex mb-4 gap-2">
        <input
          className="border p-2 flex-grow"
          placeholder="New address"
          value={newAddress}
          onChange={(e) => setNewAddress(e.target.value)}
        />
        <button className="bg-blue-500 text-white px-4 py-2" onClick={addAddress}>
          Add
        </button>
      </div>

       <ul className="space-y-2">
         {addresses.map((addr) => (
           <li
             key={addr.id}
             className="border p-2 flex justify-between items-center rounded"
           >
             <Link
               href={`/addresses/${encodeURIComponent(addr.address)}`}
               className="flex-1 flex justify-between items-center hover:text-blue-600"
             >
               <div className="font-mono">{addr.address}</div>
               <div className="text-sm text-gray-600">
                 Final Balance: {addr.final_balance}
               </div>
             </Link>
             <button
               className="text-red-500 ml-2"
               onClick={() => deleteAddress(addr.address)}
             >
               Delete
             </button>
           </li>
         ))}
       </ul>
    </main>
  );
}