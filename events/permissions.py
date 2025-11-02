from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow organizers of an event to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the organizer
        return obj.organizer == request.user

class IsPrivateEventAccessible(permissions.BasePermission):
    """
    Custom permission to restrict access to private events to invited users only.
    """
    def has_object_permission(self, request, view, obj):
        # Public events are accessible to all authenticated users
        if obj.is_public:
            return True
        
        # Private events are only accessible to the organizer and users with RSVP
        return obj.organizer == request.user or obj.rsvps.filter(user=request.user).exists()

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user