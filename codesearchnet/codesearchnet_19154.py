def changeset_info(changeset):
    """Return a dictionary with id, user, user_id, bounds, date of creation
    and all the tags of the changeset.

    Args:
        changeset: the XML string of the changeset.
    """
    keys = [tag.attrib.get('k') for tag in changeset.getchildren()]
    keys += ['id', 'user', 'uid', 'bbox', 'created_at']
    values = [tag.attrib.get('v') for tag in changeset.getchildren()]
    values += [
        changeset.get('id'), changeset.get('user'), changeset.get('uid'),
        get_bounds(changeset), changeset.get('created_at')
        ]

    return dict(zip(keys, values))