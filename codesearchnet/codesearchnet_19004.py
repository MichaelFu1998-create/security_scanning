def image_urls(self):
        """
        Combine finder_image_urls and extender_image_urls,
        remove duplicate but keep order
        """

        all_image_urls = self.finder_image_urls[:]
        for image_url in self.extender_image_urls:
            if image_url not in all_image_urls:
                all_image_urls.append(image_url)

        return all_image_urls