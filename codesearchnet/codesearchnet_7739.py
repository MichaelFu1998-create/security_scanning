def _restore_cache(gallery):
    """Restores the exif data cache from the cache file"""
    cachePath = os.path.join(gallery.settings["destination"], ".exif_cache")
    try:
        if os.path.exists(cachePath):
            with open(cachePath, "rb") as cacheFile:
                gallery.exifCache = pickle.load(cacheFile)
                logger.debug("Loaded cache with %d entries", len(gallery.exifCache))
        else:
            gallery.exifCache = {}
    except Exception as e:
        logger.warn("Could not load cache: %s", e)
        gallery.exifCache = {}