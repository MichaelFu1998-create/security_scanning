def validate(self, data):  # pylint: disable=arguments-differ
        """
        Validate that at least one of the user identifier fields has been passed in.
        """
        lms_user_id = data.get('lms_user_id')
        tpa_user_id = data.get('tpa_user_id')
        user_email = data.get('user_email')
        if not lms_user_id and not tpa_user_id and not user_email:
            raise serializers.ValidationError(
                'At least one of the following fields must be specified and map to an EnterpriseCustomerUser: '
                'lms_user_id, tpa_user_id, user_email'
            )

        return data