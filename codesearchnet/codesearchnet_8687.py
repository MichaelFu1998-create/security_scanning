def get(self, request):
        """
        GET /consent/api/v1/data_sharing_consent?username=bob&course_id=id&enterprise_customer_uuid=uuid
        *username*
            The edX username from whom to get consent.
        *course_id*
            The course for which consent is granted.
        *enterprise_customer_uuid*
            The UUID of the enterprise customer that requires consent.
        """
        try:
            consent_record = self.get_consent_record(request)
            if consent_record is None:
                return self.get_no_record_response(request)
        except ConsentAPIRequestError as invalid_request:
            return Response({'error': str(invalid_request)}, status=HTTP_400_BAD_REQUEST)

        return Response(consent_record.serialize(), status=HTTP_200_OK)