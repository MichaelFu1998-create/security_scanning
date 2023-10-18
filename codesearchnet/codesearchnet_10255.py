def store_image(cls, http_client, link_hash, src, config):
        """\
        Writes an image src http string to disk as a temporary file
        and returns the LocallyStoredImage object
        that has the info you should need on the image
        """
        # check for a cache hit already on disk
        image = cls.read_localfile(link_hash, src, config)
        if image:
            return image

        # no cache found; do something else

        # parse base64 image
        if src.startswith('data:image'):
            image = cls.write_localfile_base64(link_hash, src, config)
            return image

        # download the image
        data = http_client.fetch(src)
        if data:
            image = cls.write_localfile(data, link_hash, src, config)
            if image:
                return image

        return None