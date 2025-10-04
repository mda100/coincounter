from rest_framework import serializers
from .models import Address, Transaction

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "address", "final_balance"]
        read_only_fields = ["address"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "address", "tx_hash"]
        read_only_fields = ["address"]
