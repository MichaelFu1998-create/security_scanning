def download_item(self, item_id, token=None, revision=None):
        """
        Download an item to disk.

        :param item_id: The id of the item to be downloaded.
        :type item_id: int | long
        :param token: (optional) The authentication token of the user
            requesting the download.
        :type token: None | string
        :param revision: (optional) The revision of the item to download, this
            defaults to HEAD.
        :type revision: None | int | long
        :returns: A tuple of the filename and the content iterator.
        :rtype: (string, unknown)
        """
        parameters = dict()
        parameters['id'] = item_id
        if token:
            parameters['token'] = token
        if revision:
            parameters['revision'] = revision
        method_url = self.full_url + 'midas.item.download'
        request = requests.get(method_url,
                               params=parameters,
                               stream=True,
                               verify=self._verify_ssl_certificate)
        filename = request.headers['content-disposition'][21:].strip('"')
        return filename, request.iter_content(chunk_size=10 * 1024)