def unlink_learners(self):
        """
        Iterate over each learner and unlink inactive SAP channel learners.

        This method iterates over each enterprise learner and unlink learner
        from the enterprise if the learner is marked inactive in the related
        integrated channel.
        """
        sap_inactive_learners = self.client.get_inactive_sap_learners()
        enterprise_customer = self.enterprise_configuration.enterprise_customer
        if not sap_inactive_learners:
            LOGGER.info(
                'Enterprise customer {%s} has no SAPSF inactive learners',
                enterprise_customer.name
            )
            return

        provider_id = enterprise_customer.identity_provider
        tpa_provider = get_identity_provider(provider_id)
        if not tpa_provider:
            LOGGER.info(
                'Enterprise customer {%s} has no associated identity provider',
                enterprise_customer.name
            )
            return None

        for sap_inactive_learner in sap_inactive_learners:
            social_auth_user = get_user_from_social_auth(tpa_provider, sap_inactive_learner['studentID'])
            if not social_auth_user:
                continue

            try:
                # Unlink user email from related Enterprise Customer
                EnterpriseCustomerUser.objects.unlink_user(
                    enterprise_customer=enterprise_customer,
                    user_email=social_auth_user.email,
                )
            except (EnterpriseCustomerUser.DoesNotExist, PendingEnterpriseCustomerUser.DoesNotExist):
                LOGGER.info(
                    'Learner with email {%s} is not associated with Enterprise Customer {%s}',
                    social_auth_user.email,
                    enterprise_customer.name
                )