def redirect_if_blocked(course_run_ids, user=None, ip_address=None, url=None):
        """
        Return redirect to embargo error page if the given user is blocked.
        """
        for course_run_id in course_run_ids:
            redirect_url = embargo_api.redirect_if_blocked(
                CourseKey.from_string(course_run_id),
                user=user,
                ip_address=ip_address,
                url=url
            )
            if redirect_url:
                return redirect_url