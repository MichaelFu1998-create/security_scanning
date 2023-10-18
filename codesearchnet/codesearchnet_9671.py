def _postreceive(self):
        """Callback from Flask"""

        digest = self._get_digest()

        if digest is not None:
            sig_parts = _get_header('X-Hub-Signature').split('=', 1)
            if not isinstance(digest, six.text_type):
                digest = six.text_type(digest)

            if (len(sig_parts) < 2 or sig_parts[0] != 'sha1'
                    or not hmac.compare_digest(sig_parts[1], digest)):
                abort(400, 'Invalid signature')

        event_type = _get_header('X-Github-Event')
        data = request.get_json()

        if data is None:
            abort(400, 'Request body must contain json')

        self._logger.info(
            '%s (%s)', _format_event(event_type, data), _get_header('X-Github-Delivery'))

        for hook in self._hooks.get(event_type, []):
            hook(data)

        return '', 204