from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from gemwallets.models import GemWallet
from django.db.models import Q


@api_view(["GET"])
def get_user_transactions(request):
    """
    Retrieves a list of all user-related transactions with pagination.
    """
    gem_wallet = GemWallet.objects.get(user=request.user)

    transactions = Transaction.objects.filter(
        Q(sender=gem_wallet) | Q(receiver=gem_wallet)
    ).order_by(
        "-updated_at"
    )  # or use a timestamp field if available

    paginator = PageNumberPagination()
    paginator.page_size = 10

    paginated_transaction = paginator.paginate_queryset(transactions, request)
    serializer = TransactionSerializer(paginated_transaction, many=True)
    return paginator.get_paginated_response(serializer.data)
