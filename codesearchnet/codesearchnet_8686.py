def get_no_record_response(self, request):
        """
        Get an HTTPResponse that can be used when there's no related EnterpriseCustomer.
        """
        username, course_id, program_uuid, enterprise_customer_uuid = self.get_required_query_params(request)
        data = {
            self.REQUIRED_PARAM_USERNAME: username,
            self.REQUIRED_PARAM_ENTERPRISE_CUSTOMER: enterprise_customer_uuid,
            self.CONSENT_EXISTS: False,
            self.CONSENT_GRANTED: False,
            self.CONSENT_REQUIRED: False,
        }
        if course_id:
            data[self.REQUIRED_PARAM_COURSE_ID] = course_id

        if program_uuid:
            data[self.REQUIRED_PARAM_PROGRAM_UUID] = program_uuid

        return Response(data, status=HTTP_200_OK)