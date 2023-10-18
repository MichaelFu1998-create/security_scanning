def get_local_image(self, src):
        """\
        returns the bytes of the image file on disk
        """
        return ImageUtils.store_image(self.fetcher, self.article.link_hash, src, self.config)