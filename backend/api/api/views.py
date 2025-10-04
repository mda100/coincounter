from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from common.models import Address, Transaction
from common.serializers import AddressSerializer, TransactionSerializer
from common.external_api import fetch_address_info
from common.tasks import add_transactions_async


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().order_by("id")
    serializer_class = AddressSerializer
    lookup_field = "address"

    def create(self, request, *args, **kwargs):
        """
        POST /addresses/
        - requires 'address' field
        - populate address data from external API
        - queue transactions for async insertion
        - return populated object
        """
        address_str = request.data.get("address")

        # 400 
        if not address_str:
            return Response({"error": "address is required"}, status=status.HTTP_400_BAD_REQUEST)
        if Address.objects.filter(address=address_str).exists():
            return Response({"error": "address already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # request external API for address data
        try:
            data = fetch_address_info(address_str)
        except Exception as e:
            return Response({"error": f"external API failed: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        # post address to db
        address = Address.objects.create(
            address=address_str,
            n_tx=data.get("n_tx", 0),
            n_unredeemed=data.get("n_unredeemed", 0),
            total_received=data.get("total_received", 0),
            total_sent=data.get("total_sent", 0),
            final_balance=data.get("final_balance", 0),
        )

        # queue transactions for async insertion
        transactions = data.get("transactions", [])
        add_transactions_async.delay(address.id, transactions)

        serializer = self.get_serializer(address)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # address metadata is updated via polling

    def destroy(self, request, *args, **kwargs):
        """DEL: delete address and related transactions"""
        instance = self.get_object()
        instance.delete()
        return Response(status=204)

    @action(detail=True, methods=["get"])
    def transactions(self, request, address=None):
        """GET: paginated transactions for an address"""
        address_obj = self.get_object()
        queryset = Transaction.objects.filter(address=address_obj).order_by("-id")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TransactionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)


class TransactionCreateView(generics.CreateAPIView):
    """POST: add transaction to an address"""
    serializer_class = TransactionSerializer
    def perform_create(self, serializer):
        return serializer.save()
