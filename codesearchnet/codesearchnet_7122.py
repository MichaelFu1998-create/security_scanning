async def _pb_request(self, endpoint, request_pb, response_pb):
        """Send a Protocol Buffer formatted chat API request.

        Args:
            endpoint (str): The chat API endpoint to use.
            request_pb: The request body as a Protocol Buffer message.
            response_pb: The response body as a Protocol Buffer message.

        Raises:
            NetworkError: If the request fails.
        """
        logger.debug('Sending Protocol Buffer request %s:\n%s', endpoint,
                     request_pb)
        res = await self._base_request(
            'https://clients6.google.com/chat/v1/{}'.format(endpoint),
            'application/x-protobuf',  # Request body is Protocol Buffer.
            'proto',  # Response body is Protocol Buffer.
            request_pb.SerializeToString()
        )
        try:
            response_pb.ParseFromString(base64.b64decode(res.body))
        except binascii.Error as e:
            raise exceptions.NetworkError(
                'Failed to decode base64 response: {}'.format(e)
            )
        except google.protobuf.message.DecodeError as e:
            raise exceptions.NetworkError(
                'Failed to decode Protocol Buffer response: {}'.format(e)
            )
        logger.debug('Received Protocol Buffer response:\n%s', response_pb)
        status = response_pb.response_header.status
        if status != hangouts_pb2.RESPONSE_STATUS_OK:
            description = response_pb.response_header.error_description
            raise exceptions.NetworkError(
                'Request failed with status {}: \'{}\''
                .format(status, description)
            )