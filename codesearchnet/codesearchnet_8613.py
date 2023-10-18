def allow_request(self, request, view):
        """
        Modify throttling for service users.

        Updates throttling rate if the request is coming from the service user, and
        defaults to UserRateThrottle's configured setting otherwise.

        Updated throttling rate comes from `DEFAULT_THROTTLE_RATES` key in `REST_FRAMEWORK`
        setting. service user throttling is specified in `DEFAULT_THROTTLE_RATES` by `service_user` key

        Example Setting:
            ```
            REST_FRAMEWORK = {
                ...
                'DEFAULT_THROTTLE_RATES': {
                    ...
                    'service_user': '50/day'
                }
            }
            ```
        """
        service_users = get_service_usernames()

        # User service user throttling rates for service user.
        if request.user.username in service_users:
            self.update_throttle_scope()

        return super(ServiceUserThrottle, self).allow_request(request, view)