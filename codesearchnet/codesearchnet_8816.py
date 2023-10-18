def proxied_get(self, *args, **kwargs):
        """
        Perform the query and returns a single object matching the given keyword arguments.

        This customizes the queryset to return an instance of ``ProxyDataSharingConsent`` when
        the searched-for ``DataSharingConsent`` instance does not exist.
        """
        original_kwargs = kwargs.copy()
        if 'course_id' in kwargs:
            try:
                # Check if we have a course ID or a course run ID
                course_run_key = str(CourseKey.from_string(kwargs['course_id']))
            except InvalidKeyError:
                # The ID we have is for a course instead of a course run; fall through
                # to the second check.
                pass
            else:
                try:
                    # Try to get the record for the course run specifically
                    return self.get(*args, **kwargs)
                except DataSharingConsent.DoesNotExist:
                    # A record for the course run didn't exist, so modify the query
                    # parameters to look for just a course record on the second pass.
                    kwargs['course_id'] = parse_course_key(course_run_key)

        try:
            return self.get(*args, **kwargs)
        except DataSharingConsent.DoesNotExist:
            return ProxyDataSharingConsent(**original_kwargs)