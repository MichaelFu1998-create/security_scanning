def filter_queryset(self, request, queryset, view):
        """
        Apply incoming filters only if user is staff. If not, only filter by user's ID.
        """
        if request.user.is_staff:
            email = request.query_params.get('email', None)
            username = request.query_params.get('username', None)
            query_parameters = {}

            if email:
                query_parameters.update(email=email)
            if username:
                query_parameters.update(username=username)
            if query_parameters:
                users = User.objects.filter(**query_parameters).values_list('id', flat=True)
                queryset = queryset.filter(user_id__in=users)
        else:
            queryset = queryset.filter(user_id=request.user.id)

        return queryset