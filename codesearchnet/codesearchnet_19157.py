def get_bounds(changeset):
    """Get the bounds of the changeset and return it as a Polygon object. If
    the changeset has not coordinates (case of the changesets that deal only
    with relations), it returns an empty Polygon.

    Args:
        changeset: the XML string of the changeset.
    """
    try:
        return Polygon([
            (float(changeset.get('min_lon')), float(changeset.get('min_lat'))),
            (float(changeset.get('max_lon')), float(changeset.get('min_lat'))),
            (float(changeset.get('max_lon')), float(changeset.get('max_lat'))),
            (float(changeset.get('min_lon')), float(changeset.get('max_lat'))),
            (float(changeset.get('min_lon')), float(changeset.get('min_lat'))),
            ])
    except TypeError:
        return Polygon()