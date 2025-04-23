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


@api