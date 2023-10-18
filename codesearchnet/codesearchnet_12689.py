async def _chunked_upload(self, media, media_size,
                              path=None,
                              media_type=None,
                              media_category=None,
                              chunk_size=2**20,
                              **params):
        """
            upload media in chunks

        Parameters
        ----------
        media : file object
            a file object of the media
        media_size : int
            size of the media
        path : str, optional
            filename of the media
        media_type : str, optional
            mime type of the media
        media_category : str, optional
            twitter media category, must be used with ``media_type``
        chunk_size : int, optional
            size of a chunk in bytes
        params : dict, optional
            additional parameters of the request

        Returns
        -------
        .data_processing.PeonyResponse
            Response of the request
        """
        if isinstance(media, bytes):
            media = io.BytesIO(media)

        chunk = media.read(chunk_size)
        is_coro = asyncio.iscoroutine(chunk)

        if is_coro:
            chunk = await chunk

        if media_type is None:
            media_metadata = await utils.get_media_metadata(chunk, path)
            media_type, media_category = media_metadata
        elif media_category is None:
            media_category = utils.get_category(media_type)

        response = await self.upload.media.upload.post(
            command="INIT",
            total_bytes=media_size,
            media_type=media_type,
            media_category=media_category,
            **params
        )

        media_id = response['media_id']
        i = 0

        while chunk:
            if is_coro:
                req = self.upload.media.upload.post(command="APPEND",
                                                    media_id=media_id,
                                                    media=chunk,
                                                    segment_index=i)
                chunk, _ = await asyncio.gather(media.read(chunk_size), req)
            else:
                await self.upload.media.upload.post(command="APPEND",
                                                    media_id=media_id,
                                                    media=chunk,
                                                    segment_index=i)

                chunk = media.read(chunk_size)

            i += 1

        status = await self.upload.media.upload.post(command="FINALIZE",
                                                     media_id=media_id)

        if 'processing_info' in status:
            while status['processing_info'].get('state') != "succeeded":
                processing_info = status['processing_info']
                if processing_info.get('state') == "failed":
                    error = processing_info.get('error', {})

                    message = error.get('message', str(status))

                    raise exceptions.MediaProcessingError(data=status,
                                                          message=message,
                                                          **params)

                delay = processing_info['check_after_secs']
                await asyncio.sleep(delay)

                status = await self.upload.media.upload.get(
                    command="STATUS",
                    media_id=media_id,
                    **params
                )

        return response