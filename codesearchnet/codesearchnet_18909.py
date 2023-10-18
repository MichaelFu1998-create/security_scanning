def create_big_thumbnail(self, token, bitstream_id, item_id, width=575):
        """
        Create a big thumbnail for the given bitstream with the given width.
        It is used as the main image of the given item and shown in the item
        view page.

        :param token: A valid token for the user in question.
        :type token: string
        :param bitstream_id: The bitstream from which to create the thumbnail.
        :type bitstream_id: int | long
        :param item_id: The item on which to set the thumbnail.
        :type item_id: int | long
        :param width: (optional) The width in pixels to which to resize (aspect
            ratio will be preserved). Defaults to 575.
        :type width: int | long
        :returns: The ItemthumbnailDao object that was created.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['bitstreamId'] = bitstream_id
        parameters['itemId'] = item_id
        parameters['width'] = width
        response = self.request('midas.thumbnailcreator.create.big.thumbnail',
                                parameters)
        return response