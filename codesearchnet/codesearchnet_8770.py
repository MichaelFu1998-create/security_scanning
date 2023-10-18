def filter_queryset(self, request, queryset, view):
        """
        Filter only for the user's ID if non-staff.
        """
        if not request.user.is_staff:
            filter_kwargs = {view.USER_ID_FILTER: request.user.id}
            queryset = queryset.filter(**filter_kwargs)
        return queryset