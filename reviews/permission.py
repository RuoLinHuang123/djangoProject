from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to delete.
    """

    def has_permission(self, request, view):

        # Allow deletion only for admin users
        # Check if it's a DELETE request and if the user is staff
        if request.method == 'DELETE':
            return request.user.is_staff
        # Deny access for any other non-safe methods for non-staff users
        return True