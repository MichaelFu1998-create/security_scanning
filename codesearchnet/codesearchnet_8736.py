def redirect(self, request, *args, **kwargs):
        """
        Redirects to the appropriate view depending on where the user came from.
        """
        enterprise_customer_uuid, course_run_id, course_key, program_uuid = RouterView.get_path_variables(**kwargs)
        resource_id = course_key or course_run_id or program_uuid
        # Replace enterprise UUID and resource ID with '{}', to easily match with a path in RouterView.VIEWS. Example:
        # /enterprise/fake-uuid/course/course-v1:cool+course+2017/enroll/ -> /enterprise/{}/course/{}/enroll/
        path = re.sub('{}|{}'.format(enterprise_customer_uuid, re.escape(resource_id)), '{}', request.path)

        # Remove course_key from kwargs if it exists because delegate views are not expecting it.
        kwargs.pop('course_key', None)

        return self.VIEWS[path].as_view()(request, *args, **kwargs)