async def upload_media(self, file_,
                           media_type=None,
                           media_category=None,
                           chunked=None,
                           size_limit=None,
                           **params):
        """
            upload a media on twitter

        Parameters
        ----------
        file_ : str or pathlib.Path or file
            Path to the file or file object
        media_type : str, optional
            mime type of the media
        media_category : str, optional
            Twitter's media category of the media, must be used with
            ``media_type``
        chunked : bool, optional
            If True, force the use of the chunked upload for the media
        size_limit : int, optional
            If set, the media will be sent using a multipart upload if
            its size is over ``size_limit`` bytes
        params : dict
            parameters used when making the request

        Returns
        -------
        .data_processing.PeonyResponse
            Response of the request
        """
        if isinstance(file_, str):
            url = urlparse(file_)
            if url.scheme.startswith('http'):
                media = await self._session.get(file_)
            else:
                path = urlparse(file_).path.strip(" \"'")
                media = await utils.execute(open(path, 'rb'))
        elif hasattr(file_, 'read') or isinstance(file_, bytes):
            media = file_
        else:
            raise TypeError("upload_media input must be a file object or a "
                            "filename or binary data or an aiohttp request")

        media_size = await utils.get_size(media)
        if chunked is not None:
            size_test = False
        else:
            size_test = await self._size_test(media_size, size_limit)

        if isinstance(media, aiohttp.ClientResponse):
            # send the content of the response
            media = media.content

        if chunked or (size_test and chunked is None):
            args = media, media_size, file_, media_type, media_category
            response = await self._chunked_upload(*args, **params)
        else:
            response = await self.upload.media.upload.post(media=media,
                                                           **params)

        if not hasattr(file_, 'read') and not getattr(media, 'closed', True):
            media.close()

        return response