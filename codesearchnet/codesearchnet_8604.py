def validate_user_email(self, value):
        """
        Validates the user_email, if given, to see if an existing EnterpriseCustomerUser exists for it.

        If it does not, it does not fail validation, unlike for the other field validation methods above.
        """
        enterprise_customer = self.context.get('enterprise_customer')

        try:
            user = User.objects.get(email=value)
            return models.EnterpriseCustomerUser.objects.get(
                user_id=user.id,
                enterprise_customer=enterprise_customer
            )
        except (models.EnterpriseCustomerUser.DoesNotExist, User.DoesNotExist):
            pass

        return value