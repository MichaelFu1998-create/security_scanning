def get_image(self, image_id_or_slug):
        """
            Return a Image by its ID/Slug.
        """
        return Image.get_object(
            api_token=self.token,
            image_id_or_slug=image_id_or_slug,
        )