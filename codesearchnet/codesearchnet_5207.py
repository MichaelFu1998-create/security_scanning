def get_object(cls, api_token, image_id_or_slug):
        """
            Class method that will return an Image object by ID or slug.

            This method is used to validate the type of the image. If it is a
            number, it will be considered as an Image ID, instead if it is a
            string, it will considered as slug.
        """
        if cls._is_string(image_id_or_slug):
            image = cls(token=api_token, slug=image_id_or_slug)
            image.load(use_slug=True)
        else:
            image = cls(token=api_token, id=image_id_or_slug)
            image.load()
        return image