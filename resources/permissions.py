from rest_framework import permissions


READ_ONLY_METHODS = ["GET"]


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in READ_ONLY_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in READ_ONLY_METHODS