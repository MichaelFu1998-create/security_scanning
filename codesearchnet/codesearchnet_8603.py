def validate_tpa_user_id(self, value):
        """
        Validates the tpa_user_id, if is given, to see if there is an existing EnterpriseCustomerUser for it.

        It first uses the third party auth api to find the associated username to do the lookup.
        """
        enterprise_customer = self.context.get('enterprise_customer')

        try:
            tpa_client = ThirdPartyAuthApiClient()
            username = tpa_client.get_username_from_remote_id(
                enterprise_customer.identity_provider, value
            )
            user = User.objects.get(username=username)
            return models.EnterpriseCustomerUser.objects.get(
                user_id=user.id,
                enterprise_customer=enterprise_customer
            )
        except (models.EnterpriseCustomerUser.DoesNotExist, User.DoesNotExist):
            pass

        return None