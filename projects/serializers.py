from rest_framework import serializers

from .models import Project, RegradeRequest
from .exceptions import InvalidCodeException, DuplicateRegradeException
from users.models import User


class RegradeSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    csid = serializers.SlugRelatedField(many=False, slug_field="csid", allow_null=False, queryset=User.objects.all(), write_only=True)
    commit = serializers.CharField(max_length=40, min_length=40)
    code = serializers.CharField(write_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    def validate(self, attrs):
        code = attrs.get("code")
        user = attrs.get("csid")
        commit = attrs.get("commit")
        project = attrs.get("project")

        if code != user.code:
            raise InvalidCodeException()

        if RegradeRequest.objects.filter(commit=commit, project=project, user=user).exists():
            raise DuplicateRegradeException()

        return attrs

    def create(self, validated_data):
        user = validated_data.get("csid")
        commit = validated_data.get("commit")
        project = validated_data.get("project")

        return RegradeRequest.objects.create(user=user, commit=commit, project=project)
