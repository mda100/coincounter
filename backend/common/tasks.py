from celery import shared_task
from .models import Address, Transaction
from .external_api import fetch_address_info

@shared_task
def add_transactions_async(address_id, transactions):
    try:
        address = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        print(f"Address with id {address_id} not found")
        return

    for i, tx in enumerate(transactions):
        print(f"Processing transaction {i+1}/{len(transactions)}")
        obj, created = Transaction.objects.get_or_create(
            tx_hash=tx["hash"],
            defaults={
                "address": address,
                "version": tx.get("version") or 1,
                "size": tx.get("size") or 0,
                "block_height": tx.get("block_height") or 0,
                "tx_index": tx.get("tx_index") or "0",
            }
        )

@shared_task
def poll_all_addresses():
    """
    Iterates over addresses in the database, fetches updated data from the
    blockchain API, updates address metadata, and queues new transactions for async insertion.
    """
    import time
    
    addresses = Address.objects.all()
    print(f"Polling {addresses.count()} addresses...")

    for i, address in enumerate(addresses):
        try:
            print(f"Polling address {i+1}/{addresses.count()}: {address.address}")
            data = fetch_address_info(address.address)
            
            # update address metadata
            address.n_tx = data.get("n_tx", address.n_tx)
            address.n_unredeemed = data.get("n_unredeemed", address.n_unredeemed)
            address.total_received = data.get("total_received", address.total_received)
            address.total_sent = data.get("total_sent", address.total_sent)
            address.final_balance = data.get("final_balance", address.final_balance)
            address.save()
            
            # queue new transactions for async processing
            transactions = data.get("transactions", [])
            if transactions:
                add_transactions_async.delay(address.id, transactions)
                print(f"Queued {len(transactions)} transactions for address {address.address}")
             
        except Exception as e:
            print(f"Error polling address {address.address}: {str(e)}")
            time.sleep(10)