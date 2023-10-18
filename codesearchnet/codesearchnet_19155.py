def get_changeset(changeset):
    """Get the changeset using the OSM API and return the content as a XML
    ElementTree.

    Args:
        changeset: the id of the changeset.
    """
    url = 'https://www.openstreetmap.org/api/0.6/changeset/{}/download'.format(
        changeset
        )
    return ET.fromstring(requests.get(url).content)