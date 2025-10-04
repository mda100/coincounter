from django.db import models

#https://www.blockchain.com/explorer/api/blockchain_api

class Address(models.Model):
    # fields are populated by external API polling
    address = models.CharField(max_length=64, unique=True, db_index=True)
    n_tx = models.IntegerField()
    n_unredeemed = models.IntegerField(null=True, blank=True)
    total_received = models.BigIntegerField(null=True, blank=True)
    total_sent = models.BigIntegerField(null=True, blank=True)
    final_balance = models.BigIntegerField(null=True, blank=True)

class Transaction(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    tx_hash = models.CharField(max_length=64, unique=True, db_index=True)
    version = models.IntegerField()
    lock_time = models.CharField(max_length=64, null=True, blank=True)
    size = models.IntegerField()
    relayed_by = models.GenericIPAddressField(null=True, blank=True)
    block_height = models.IntegerField()
    tx_index = models.CharField(max_length=64)
