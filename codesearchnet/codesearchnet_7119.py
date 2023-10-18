def _get_upload_session_status(res):
        """Parse the image upload response to obtain status.

        Args:
            res: http_utils.FetchResponse instance, the upload response

        Returns:
            dict, sessionStatus of the response

        Raises:
            hangups.NetworkError: If the upload request failed.
        """
        response = json.loads(res.body.decode())
        if 'sessionStatus' not in response:
            try:
                info = (
                    response['errorMessage']['additionalInfo']
                    ['uploader_service.GoogleRupioAdditionalInfo']
                    ['completionInfo']['customerSpecificInfo']
                )
                reason = '{} : {}'.format(info['status'], info['message'])
            except KeyError:
                reason = 'unknown reason'
            raise exceptions.NetworkError('image upload failed: {}'.format(
                reason
            ))
        return response['sessionStatus']