def get_disk_image_by_name(pbclient, location, image_name):
    """
    Returns all disk images within a location with a given image name.
    The name must match exactly.
    The list may be empty.
    """
    all_images = pbclient.list_images()
    matching = [i for i in all_images['items'] if
                i['properties']['name'] == image_name and
                i['properties']['imageType'] == "HDD" and
                i['properties']['location'] == location]
    return matching