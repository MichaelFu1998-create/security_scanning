def load(self, use_slug=False):
        """
            Load slug.

            Loads by id, or by slug if id is not present or use slug is True.
        """
        identifier = None
        if use_slug or not self.id:
            identifier = self.slug
        else:
            identifier = self.id
        if not identifier:
            raise NotFoundError("One of self.id or self.slug must be set.")
        data = self.get_data("images/%s" % identifier)
        image_dict = data['image']

        # Setting the attribute values
        for attr in image_dict.keys():
            setattr(self, attr, image_dict[attr])

        return self