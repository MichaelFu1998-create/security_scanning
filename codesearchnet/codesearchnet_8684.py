def get_consent_record(self, request):
        """
        Get the consent record relevant to the request at hand.
        """
        username, course_id, program_uuid, enterprise_customer_uuid = self.get_required_query_params(request)
        return get_data_sharing_consent(
            username,
            enterprise_customer_uuid,
            course_id=course_id,
            program_uuid=program_uuid
        )