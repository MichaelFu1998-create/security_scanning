async def upload_image(self, image_file, filename=None, *,
                           return_uploaded_image=False):
        """Upload an image that can be later attached to a chat message.

        Args:
            image_file: A file-like object containing an image.
            filename (str): (optional) Custom name for the uploaded file.
            return_uploaded_image (bool): (optional) If True, return
                :class:`.UploadedImage` instead of image ID. Defaults to False.

        Raises:
            hangups.NetworkError: If the upload request failed.

        Returns:
            :class:`.UploadedImage` instance, or ID of the uploaded image.
        """
        image_filename = filename or os.path.basename(image_file.name)
        image_data = image_file.read()

        # request an upload URL
        res = await self._base_request(
            IMAGE_UPLOAD_URL,
            'application/x-www-form-urlencoded;charset=UTF-8', 'json',
            json.dumps({
                "protocolVersion": "0.8",
                "createSessionRequest": {
                    "fields": [{
                        "external": {
                            "name": "file",
                            "filename": image_filename,
                            "put": {},
                            "size": len(image_data)
                        }
                    }]
                }
            })
        )

        try:
            upload_url = self._get_upload_session_status(res)[
                'externalFieldTransfers'
            ][0]['putInfo']['url']
        except KeyError:
            raise exceptions.NetworkError(
                'image upload failed: can not acquire an upload url'
            )

        # upload the image data using the upload_url to get the upload info
        res = await self._base_request(
            upload_url, 'application/octet-stream', 'json', image_data
        )

        try:
            raw_info = (
                self._get_upload_session_status(res)['additionalInfo']
                ['uploader_service.GoogleRupioAdditionalInfo']
                ['completionInfo']['customerSpecificInfo']
            )
            image_id = raw_info['photoid']
            url = raw_info['url']
        except KeyError:
            raise exceptions.NetworkError(
                'image upload failed: can not fetch upload info'
            )

        result = UploadedImage(image_id=image_id, url=url)
        return result if return_uploaded_image else result.image_id