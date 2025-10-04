from celery import shared_task
from .models import Address, Transaction
from .external_api import fetch_address_info

@shared_task
def add_transactions_async(address_id, transactions):
    try:
        address = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        return

    created_count = 0
    for tx in transactions:
        obj, created = Transaction.objects.get_or_create(
            tx_hash=tx["hash"],
            defaults={
                "address": address,
                "version": tx.get("version"),
                "size": tx.get("size"),
                "block_height": tx.get("block_height"),
                "tx_index": tx.get("tx_index"),
            }
        )
        if created:
            created_count += 1

@shared_task
def poll_all_addresses():
    """
    Iterates over addresses in the database, fetches updated data from the
    blockchain API, updates address metadata, and queues new transactions for async insertion.
    """
    addresses = Address.objects.all()

    for address in addresses:
        try:
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
             
        except Exception as e:
            pass