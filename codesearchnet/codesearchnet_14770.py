def is_isonet_vif(vif):
    """Determine if a vif is on isonet

    Returns True if a vif belongs to an isolated network by checking
    for a nicira interface id.
    """
    nicira_iface_id = vif.record.get('other_config').get('nicira-iface-id')

    if nicira_iface_id:
        return True

    return False