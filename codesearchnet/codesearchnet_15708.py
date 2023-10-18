def valid_content_type(self, content_type, accept):
        """Check that the server is returning a valid Content-Type

        Args:
            content_type (str): ``Content-Type:`` header value
            accept (str): media type to include in the ``Accept:`` header.

        """
        accept_tokens = accept.replace(' ', '').split(';')
        content_type_tokens = content_type.replace(' ', '').split(';')

        return (
            all(elem in content_type_tokens for elem in accept_tokens) and
            (content_type_tokens[0] == 'application/vnd.oasis.taxii+json' or
             content_type_tokens[0] == 'application/vnd.oasis.stix+json')
        )