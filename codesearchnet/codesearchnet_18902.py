def generate_upload_token(self, token, item_id, filename, checksum=None):
        """
        Generate a token to use for upload.

        Midas Server uses a individual token for each upload. The token
        corresponds to the file specified and that file only. Passing the MD5
        checksum allows the server to determine if the file is already in the
        asset store.

        If :param:`checksum` is passed and the token returned is blank, the
        server already has this file and there is no need to follow this
        call with a call to `perform_upload`, as the passed in file will have
        been added as a bitstream to the item's latest revision, creating a
        new revision if one doesn't exist.

        :param token: A valid token for the user in question.
        :type token: string
        :param item_id: The id of the item in which to upload the file as a
            bitstream.
        :type item_id: int | long
        :param filename: The name of the file to generate the upload token for.
        :type filename: string
        :param checksum: (optional) The checksum of the file to upload.
        :type checksum: None | string
        :returns: String of the upload token.
        :rtype: string
        """
        parameters = dict()
        parameters['token'] = token
        parameters['itemid'] = item_id
        parameters['filename'] = filename
        if checksum is not None:
            parameters['checksum'] = checksum
        response = self.request('midas.upload.generatetoken', parameters)
        return response['token']