def has_add_permission(self, request):
        """ Can add this object """
        return request.user.is_authenticated and request.user.is_active and request.user.is_staff