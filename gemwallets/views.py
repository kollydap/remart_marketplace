from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from gemwallets.models import GemWallet
from gemwallets.serializers import GemWalletSerializer


# GET logged-in user's wallet balance
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_wallet(request):
    """
    Retrieves the wallet balance for the logged-in user.
    """
    try:
        wallet = GemWallet.objects.get(user=request.user)
    except GemWallet.DoesNotExist:
        return Response(
            {"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = GemWalletSerializer(wallet)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transfer_to_user(request):
    """
    Retrieves the wallet balance for the logged-in user.
    """
    try:
        wallet = GemWallet.objects.get(user=request.user)
    except GemWallet.DoesNotExist:
        return Response(
            {"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND
        )
    try:
        recipient_wallet = GemWallet.objects.get(
            user__username=request.data["username"]
        )
    except GemWallet.DoesNotExist:
        return Response(
            {"error": "Recipient wallet not found."}, status=status.HTTP_404_NOT_FOUND
        )
    try:
        amount = float(request.data["amount"])
    except (ValueError, TypeError):
        return Response(
            {"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST
        )
    if amount <= 0:
        return Response(
            {"error": "Amount must be greater than zero."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if wallet.balance < amount:
        return Response(
            {"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST
        )
    wallet.balance -= amount
    recipient_wallet.balance += amount
    wallet.save()
    recipient_wallet.save()

    return Response({"message": "transfer successful"}, status=status.HTTP_200_OK)
