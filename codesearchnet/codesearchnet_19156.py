def get_metadata(changeset):
    """Get the metadata of a changeset using the OSM API and return it as a XML
    ElementTree.

    Args:
        changeset: the id of the changeset.
    """
    url = 'https://www.openstreetmap.org/api/0.6/changeset/{}'.format(changeset)
    return ET.fromstring(requests.get(url).content).getchildren()[0]