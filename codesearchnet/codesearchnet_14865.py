def sg_gather_associated_ports(context, group):
    """Gather all ports associated to security group.

    Returns:
    * list, or None
    """
    if not group:
        return None
    if not hasattr(group, "ports") or len(group.ports) <= 0:
        return []
    return group.ports