def filter_nomedia(album, settings=None):
    """Removes all filtered Media and subdirs from an Album"""
    nomediapath = os.path.join(album.src_path, ".nomedia")

    if os.path.isfile(nomediapath):
        if os.path.getsize(nomediapath) == 0:
            logger.info("Ignoring album '%s' because of present 0-byte "
                        ".nomedia file", album.name)

            # subdirs have been added to the gallery already, remove them
            # there, too
            _remove_albums_with_subdirs(album.gallery.albums, [album.path])
            try:
                os.rmdir(album.dst_path)
            except OSError as e:
                # directory was created and populated with images in a
                # previous run => keep it
                pass

            # cannot set albums => empty subdirs so that no albums are
            # generated
            album.subdirs = []
            album.medias = []

        else:
            with open(nomediapath, "r") as nomediaFile:
                logger.info("Found a .nomedia file in %s, ignoring its "
                            "entries", album.name)
                ignored = nomediaFile.read().split("\n")

                album.medias = [media for media in album.medias
                                if media.src_filename not in ignored]
                album.subdirs = [dirname for dirname in album.subdirs
                                 if dirname not in ignored]

                # subdirs have been added to the gallery already, remove
                # them there, too
                _remove_albums_with_subdirs(album.gallery.albums,
                                            ignored, album.path + os.path.sep)