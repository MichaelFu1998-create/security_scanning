def get_enterprise_customer_for_user(auth_user):
    """
    Return enterprise customer instance for given user.

    Some users are associated with an enterprise customer via `EnterpriseCustomerUser` model,
        1. if given user is associated with any enterprise customer, return enterprise customer.
        2. otherwise return `None`.

    Arguments:
        auth_user (contrib.auth.User): Django User

    Returns:
        (EnterpriseCustomer): enterprise customer associated with the current user.

    """
    EnterpriseCustomerUser = apps.get_model('enterprise', 'EnterpriseCustomerUser')  # pylint: disable=invalid-name
    try:
        return EnterpriseCustomerUser.objects.get(user_id=auth_user.id).enterprise_customer  # pylint: disable=no-member
    except EnterpriseCustomerUser.DoesNotExist:
        return None