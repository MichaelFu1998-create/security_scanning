def _negotiateHandler(self, request):
        """
        Negotiate a handler based on the content types acceptable to the
        client.

        :rtype: 2-`tuple` of `twisted.web.iweb.IResource` and `bytes`
        :return: Pair of a resource and the content type.
        """
        accept = _parseAccept(request.requestHeaders.getRawHeaders('Accept'))
        for contentType in accept.keys():
            handler = self._acceptHandlers.get(contentType.lower())
            if handler is not None:
                return handler, handler.contentType

        if self._fallback:
            handler = self._handlers[0]
            return handler, handler.contentType
        return NotAcceptable(), None