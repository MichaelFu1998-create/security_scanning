def get_data_sharing_consent(username, enterprise_customer_uuid, course_id=None, program_uuid=None):
    """
    Get the data sharing consent object associated with a certain user, enterprise customer, and other scope.

    :param username: The user that grants consent
    :param enterprise_customer_uuid: The consent requester
    :param course_id (optional): A course ID to which consent may be related
    :param program_uuid (optional): A program to which consent may be related
    :return: The data sharing consent object, or None if the enterprise customer for the given UUID does not exist.
    """
    EnterpriseCustomer = apps.get_model('enterprise', 'EnterpriseCustomer')  # pylint: disable=invalid-name
    try:
        if course_id:
            return get_course_data_sharing_consent(username, course_id, enterprise_customer_uuid)
        return get_program_data_sharing_consent(username, program_uuid, enterprise_customer_uuid)
    except EnterpriseCustomer.DoesNotExist:
        return None