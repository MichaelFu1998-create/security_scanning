async def _base_request(self, url, content_type, response_type, data):
        """Send a generic authenticated POST request.

        Args:
            url (str): URL of request.
            content_type (str): Request content type.
            response_type (str): The desired response format. Valid options
                are: 'json' (JSON), 'protojson' (pblite), and 'proto' (binary
                Protocol Buffer). 'proto' requires manually setting an extra
                header 'X-Goog-Encode-Response-If-Executable: base64'.
            data (str): Request body data.

        Returns:
            FetchResponse: Response containing HTTP code, cookies, and body.

        Raises:
            NetworkError: If the request fails.
        """
        headers = {
            'content-type': content_type,
            # This header is required for Protocol Buffer responses. It causes
            # them to be base64 encoded:
            'X-Goog-Encode-Response-If-Executable': 'base64',
        }
        params = {
            # "alternative representation type" (desired response format).
            'alt': response_type,
            # API key (required to avoid 403 Forbidden "Daily Limit for
            # Unauthenticated Use Exceeded. Continued use requires signup").
            'key': API_KEY,
        }
        res = await self._session.fetch(
            'post', url, headers=headers, params=params, data=data,
        )
        return res