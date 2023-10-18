def validate_lms_user_id(self, value):
        """
        Validates the lms_user_id, if is given, to see if there is an existing EnterpriseCustomerUser for it.
        """
        enterprise_customer = self.context.get('enterprise_customer')

        try:
            # Ensure the given user is associated with the enterprise.
            return models.EnterpriseCustomerUser.objects.get(
                user_id=value,
                enterprise_customer=enterprise_customer
            )
        except models.EnterpriseCustomerUser.DoesNotExist:
            pass

        return None