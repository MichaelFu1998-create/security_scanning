def get_enterprise_customer(uuid):
        """
        Returns the enterprise customer requested for the given uuid, None if not.

        Raises CommandError if uuid is invalid.
        """
        if uuid is None:
            return None
        try:
            return EnterpriseCustomer.active_customers.get(uuid=uuid)
        except EnterpriseCustomer.DoesNotExist:
            raise CommandError(
                _('Enterprise customer {uuid} not found, or not active').format(uuid=uuid))