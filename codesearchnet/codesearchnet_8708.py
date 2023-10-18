def clean(self):
        """
        Final validations of model fields.

        1. Validate that selected site for enterprise customer matches with the selected identity provider's site.
        """
        super(EnterpriseCustomerIdentityProviderAdminForm, self).clean()

        provider_id = self.cleaned_data.get('provider_id', None)
        enterprise_customer = self.cleaned_data.get('enterprise_customer', None)

        if provider_id is None or enterprise_customer is None:
            # field validation for either provider_id or enterprise_customer has already raised
            # a validation error.
            return

        identity_provider = utils.get_identity_provider(provider_id)
        if not identity_provider:
            # This should not happen, as identity providers displayed in drop down are fetched dynamically.
            message = _(
                "The specified Identity Provider does not exist. For more "
                "information, contact a system administrator.",
            )
            # Log message for debugging
            logger.exception(message)

            raise ValidationError(message)

        if identity_provider and identity_provider.site != enterprise_customer.site:
            raise ValidationError(
                _(
                    "The site for the selected identity provider "
                    "({identity_provider_site}) does not match the site for "
                    "this enterprise customer ({enterprise_customer_site}). "
                    "To correct this problem, select a site that has a domain "
                    "of '{identity_provider_site}', or update the identity "
                    "provider to '{enterprise_customer_site}'."
                ).format(
                    enterprise_customer_site=enterprise_customer.site,
                    identity_provider_site=identity_provider.site,
                ),
            )