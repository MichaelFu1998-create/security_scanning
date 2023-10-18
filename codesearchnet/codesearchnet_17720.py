def check_status(content, response):
        """
        Check the response that is returned for known exceptions and errors.
        :param response: Response that is returned from the call.
        :raise:
         MalformedRequestException if `response.status` is 400
         UnauthorisedException if `response.status` is 401
         NotFoundException if `response.status` is 404
         UnacceptableContentException if `response.status` is 406
         InvalidRequestException if `response.status` is 422
         RateLimitException if `response.status` is 429
         ServerException if `response.status` > 500
        """

        if response.status == 400:
            raise MalformedRequestException(content, response)

        if response.status == 401:
            raise UnauthorisedException(content, response)

        if response.status == 404:
            raise NotFoundException(content, response)

        if response.status == 406:
            raise UnacceptableContentException(content, response)

        if response.status == 422:
            raise InvalidRequestException(content, response)

        if response.status == 429:
            raise RateLimitException(content, response)

        if response.status >= 500:
            raise ServerException(content, response)