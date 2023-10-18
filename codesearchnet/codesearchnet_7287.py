def remove_images():
    """Removes all dangling images as well as all images referenced in a dusty spec; forceful removal is not used"""
    client = get_docker_client()
    removed = _remove_dangling_images()
    dusty_images = get_dusty_images()
    all_images = client.images(all=True)
    for image in all_images:
        if set(image['RepoTags']).intersection(dusty_images):
            try:
                client.remove_image(image['Id'])
            except Exception as e:
                logging.info("Couldn't remove image {}".format(image['RepoTags']))
            else:
                log_to_client("Removed Image {}".format(image['RepoTags']))
                removed.append(image)
    return removed