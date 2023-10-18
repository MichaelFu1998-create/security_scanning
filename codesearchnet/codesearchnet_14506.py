def update_image(self, image_id, **kwargs):
        """
        Replace all properties of an image.

        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        response = self._perform_request(url='/images/' + image_id,
                                         method='PATCH',
                                         data=json.dumps(data))
        return response