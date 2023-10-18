def _get_base(group, **conn):
    """Fetch the base IAM Group."""
    group['_version'] = 1

    # Get the initial group details (only needed if we didn't grab the users):
    group.update(get_group_api(group['GroupName'], users=False, **conn)['Group'])

    # Cast CreateDate from a datetime to something JSON serializable.
    group['CreateDate'] = get_iso_string(group['CreateDate'])
    return group