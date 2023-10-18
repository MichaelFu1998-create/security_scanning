def get_group_name(id_group):
    """Used for breadcrumb dynamic_list_constructor."""
    group = Group.query.get(id_group)
    if group is not None:
        return group.name