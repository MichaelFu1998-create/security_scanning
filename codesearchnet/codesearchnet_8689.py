def delete(self, request):
        """
        DELETE /consent/api/v1/data_sharing_consent

        Requires a JSON object of the following format:
        >>> {
        >>>     "username": "bob",
        >>>     "course_id": "course-v1:edX+DemoX+Demo_Course",
        >>>     "enterprise_customer_uuid": "enterprise-uuid-goes-right-here"
        >>> }

        Keys:
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

            # We're fine with proactively refusing consent, even when there's no actual
            # requirement for consent yet.
            consent_record.granted = False

            # Models don't have return values when saving, but ProxyDataSharingConsent
            # objects do - they should return either a model instance, or another instance
            # of ProxyDataSharingConsent if representing a multi-course consent record.
            consent_record = consent_record.save() or consent_record

        except ConsentAPIRequestError as invalid_request:
            return Response({'error': str(invalid_request)}, status=HTTP_400_BAD_REQUEST)

        return Response(consent_record.serialize())