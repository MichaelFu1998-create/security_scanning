def handle_enterprise_logistration(backend, user, **kwargs):
    """
    Perform the linking of user in the process of logging to the Enterprise Customer.

    Args:
        backend: The class handling the SSO interaction (SAML, OAuth, etc)
        user: The user object in the process of being logged in with
        **kwargs: Any remaining pipeline variables

    """
    request = backend.strategy.request
    enterprise_customer = get_enterprise_customer_for_running_pipeline(
        request,
        {
            'backend': backend.name,
            'kwargs': kwargs
        }
    )
    if enterprise_customer is None:
        # This pipeline element is not being activated as a part of an Enterprise logistration
        return

    # proceed with the creation of a link between the user and the enterprise customer, then exit.
    enterprise_customer_user, _ = EnterpriseCustomerUser.objects.update_or_create(
        enterprise_customer=enterprise_customer,
        user_id=user.id
    )
    enterprise_customer_user.update_session(request)