def get_required_query_params(self, request):
        """
        Gets ``username``, ``course_id``, and ``enterprise_customer_uuid``,
        which are the relevant query parameters for this API endpoint.

        :param request: The request to this endpoint.
        :return: The ``username``, ``course_id``, and ``enterprise_customer_uuid`` from the request.
        """
        username = get_request_value(request, self.REQUIRED_PARAM_USERNAME, '')
        course_id = get_request_value(request, self.REQUIRED_PARAM_COURSE_ID, '')
        program_uuid = get_request_value(request, self.REQUIRED_PARAM_PROGRAM_UUID, '')
        enterprise_customer_uuid = get_request_value(request, self.REQUIRED_PARAM_ENTERPRISE_CUSTOMER)
        if not (username and (course_id or program_uuid) and enterprise_customer_uuid):
            raise ConsentAPIRequestError(
                self.get_missing_params_message([
                    ("'username'", bool(username)),
                    ("'enterprise_customer_uuid'", bool(enterprise_customer_uuid)),
                    ("one of 'course_id' or 'program_uuid'", bool(course_id or program_uuid)),
                ])
            )
        return username, course_id, program_uuid, enterprise_customer_uuid