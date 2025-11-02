from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.organizer == request.user

class IsPrivateEventAccessible(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        
        return obj.organizer == request.user or obj.rsvps.filter(user=request.user).exists()

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user