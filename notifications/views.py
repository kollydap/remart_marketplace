from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework.pagination import PageNumberPagination


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_notifications(request):
    notifications = Notification.objects.all().filter(user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_notifications = paginator.paginate_queryset(notifications, request)
    serializer = NotificationSerializer(paginated_notifications, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_a_notification(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response(
            {"message": "❌ Oops! That Notification has vanished."},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = NotificationSerializer(notification)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_notification(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response(
            {"message": "❌ Oops! That Notification has vanished."},
            status=status.HTTP_404_NOT_FOUND,
        )
    notification.delete()
    return Response(
        {"message": "deleted successfully."}, status=status.HTTP_204_NO_CONTENT
    )
    
