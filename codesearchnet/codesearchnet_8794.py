def _build_context(self, request, enterprise_customer_uuid):
        """
        Build common context parts used by different handlers in this view.
        """
        enterprise_customer = EnterpriseCustomer.objects.get(uuid=enterprise_customer_uuid)  # pylint: disable=no-member

        context = {
            self.ContextParameters.ENTERPRISE_CUSTOMER: enterprise_customer,
        }
        context.update(admin.site.each_context(request))
        context.update(self._build_admin_context(request, enterprise_customer))
        return context