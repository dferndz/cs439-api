from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import RegradeSerializer


class RegradeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = RegradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        regrade = serializer.save()

        return Response(data=RegradeSerializer(regrade).data)
