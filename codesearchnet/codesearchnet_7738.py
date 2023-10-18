def load_exif(album):
    """Loads the exif data of all images in an album from cache"""
    if not hasattr(album.gallery, "exifCache"):
        _restore_cache(album.gallery)
    cache = album.gallery.exifCache

    for media in album.medias:
        if media.type == "image":
            key = os.path.join(media.path, media.filename)
            if key in cache:
                media.exif = cache[key]