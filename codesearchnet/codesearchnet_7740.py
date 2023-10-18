def save_cache(gallery):
    """Stores the exif data of all images in the gallery"""

    if hasattr(gallery, "exifCache"):
        cache = gallery.exifCache
    else:
        cache = gallery.exifCache = {}

    for album in gallery.albums.values():
        for image in album.images:
            cache[os.path.join(image.path, image.filename)] = image.exif

    cachePath = os.path.join(gallery.settings["destination"], ".exif_cache")

    if len(cache) == 0:
        if os.path.exists(cachePath):
            os.remove(cachePath)
        return

    try:
        with open(cachePath, "wb") as cacheFile:
            pickle.dump(cache, cacheFile)
            logger.debug("Stored cache with %d entries", len(gallery.exifCache))
    except Exception as e:
        logger.warn("Could not store cache: %s", e)
        os.remove(cachePath)