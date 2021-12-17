from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import RegradeSerializer, ProjectSerializer
from .models import Project


class RegradeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = RegradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        regrade = serializer.save()

        return Response(data=RegradeSerializer(regrade).data)


class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializer

    def list(self, request):
        serializer = self.serializer_class(Project.objects.all(), many=True)
        return Response(data=serializer.data)
