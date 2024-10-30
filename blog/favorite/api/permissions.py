from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):

    def has_permission(self, request, view):
        print("has_permission çalıştı......")
        print(request.user.is_authenticated)
        print(request.user)
        return request.user and request.user.is_authenticated

    message = "You must be the owner"
    def has_object_permission(self, request, view, obj):
        print("has_object_permission çalıştı.")
        return (obj.user == request.user)