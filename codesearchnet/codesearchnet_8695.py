def validate_email_to_link(email, raw_email=None, message_template=None, ignore_existing=False):
    """
    Validate email to be linked to Enterprise Customer.

    Performs two checks:
        * Checks that email is valid
        * Checks that it is not already linked to any Enterprise Customer

    Arguments:
        email (str): user email to link
        raw_email (str): raw value as it was passed by user - used in error message.
        message_template (str): Validation error template string.
        ignore_existing (bool): If True to skip the check for an existing Enterprise Customer

    Raises:
        ValidationError: if email is invalid or already linked to Enterprise Customer.

    Returns:
        bool: Whether or not there is an existing record with the same email address.
    """
    raw_email = raw_email if raw_email is not None else email
    message_template = message_template if message_template is not None else ValidationMessages.INVALID_EMAIL
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(message_template.format(argument=raw_email))

    existing_record = EnterpriseCustomerUser.objects.get_link_by_email(email)
    if existing_record and not ignore_existing:
        raise ValidationError(ValidationMessages.USER_ALREADY_REGISTERED.format(
            email=email, ec_name=existing_record.enterprise_customer.name
        ))
    return existing_record or False