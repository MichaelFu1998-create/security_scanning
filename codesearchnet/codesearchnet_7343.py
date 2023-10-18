def registry_from_image(image_name):
    """Returns the Docker registry host associated with
    a given image name."""
    if '/' not in image_name: # official image
        return constants.PUBLIC_DOCKER_REGISTRY
    prefix = image_name.split('/')[0]
    if '.' not in prefix: # user image on official repository, e.g. thieman/clojure
        return constants.PUBLIC_DOCKER_REGISTRY
    return prefix