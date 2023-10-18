def organization_data_is_valid(organization_data):
    """
    Organization data validation
    """
    if organization_data is None:
        return False
    if 'id' in organization_data and not organization_data.get('id'):
        return False
    if 'name' in organization_data and not organization_data.get('name'):
        return False
    return True