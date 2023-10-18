def delete_image(self, image_id):
        """
        Removes only user created images.

        :param      image_id: The unique ID of the image.
        :type       image_id: ``str``

        """
        response = self._perform_request(url='/images/' + image_id,
                                         method='DELETE')
        return response