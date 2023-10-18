def get_top_assets(self):
        """
        Gets images and videos to populate top assets.

        Map is built separately.
        """
        images = self.get_all_images()[0:14]
        video = []
        if supports_video:
            video = self.eventvideo_set.all()[0:10]

        return list(chain(images, video))[0:15]