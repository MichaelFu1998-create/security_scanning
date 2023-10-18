def has_delete_permission(self, request):
        """ Can delete this object """
        return request.user.is_authenticated and request.user.is_active and request.user.is_superuser