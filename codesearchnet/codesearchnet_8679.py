def get_program_data_sharing_consent(username, program_uuid, enterprise_customer_uuid):
    """
    Get the data sharing consent object associated with a certain user of a customer for a program.

    :param username: The user that grants consent.
    :param program_uuid: The program for which consent is granted.
    :param enterprise_customer_uuid: The consent requester.
    :return: The data sharing consent object
    """
    enterprise_customer = get_enterprise_customer(enterprise_customer_uuid)
    discovery_client = CourseCatalogApiServiceClient(enterprise_customer.site)
    course_ids = discovery_client.get_program_course_keys(program_uuid)
    child_consents = (
        get_data_sharing_consent(username, enterprise_customer_uuid, course_id=individual_course_id)
        for individual_course_id in course_ids
    )
    return ProxyDataSharingConsent.from_children(program_uuid, *child_consents)