def has_edit_permission(self, request):
        """ Can edit this object """
        return request.user.is_authenticated and request.user.is_active and request.user.is_staff