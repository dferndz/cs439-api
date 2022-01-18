from rest_framework import viewsets
from .models import Resource
from .serializers import ResourceSerializer
from .permissions import ReadOnly


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [ReadOnly]
    queryset = Resource.objects.all()
