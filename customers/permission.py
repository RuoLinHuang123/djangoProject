from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it, 
    admins full access, and create operations to be public.
    """

    def has_permission(self, request, view):
        # Allow all read-only requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow create operations to be public
        if request.method == 'POST':
            return True
        # Allow full access to admin users
        if request.user and request.user.is_staff:
            return True

        # For actions on 'me', check if the user is authenticated
        # Note: 'me' could be a specific action in your ViewSet
        # that requires the user to be the owner of the data.
        if view.action == 'me':
            return request.user.is_authenticated

        return False

    