def view(cls, request, response):
        """
        Entry-point of the request / response cycle; Handles resource creation
        and delegation.

        @param[in] requset
            The HTTP request object; containing accessors for information
            about the request.

        @param[in] response
            The HTTP response object; contains accessors for modifying
            the information that will be sent to the client.
        """
        # Determine if we need to redirect.
        test = cls.meta.trailing_slash
        if test ^ request.path.endswith('/'):
            # Construct a new URL by removing or adding the trailing slash.
            path = request.path + '/' if test else request.path[:-1]
            response['Location'] = '{}://{}{}{}{}'.format(
                request.protocol.lower(),
                request.host,
                request.mount_point,
                path,
                '?' + request.query if request.query else '')

            # Redirect to the version with the correct trailing slash.
            return cls.redirect(request, response)

        try:
            # Instantiate the resource.
            obj = cls(request, response)

            # Bind the request and response objects to the constructed
            # resource.
            request.bind(obj)
            response.bind(obj)

            # Bind the request object to the resource.
            # This is used to facilitate the serializer and deserializer.
            obj._request = request

            # Initiate the dispatch cycle and handle its result on
            # synchronous requests.
            result = obj.dispatch(request, response)

            if not response.asynchronous:
                # There is several things that dispatch is allowed to return.
                if (isinstance(result, collections.Iterable) and
                        not isinstance(result, six.string_types)):
                    # Return the stream generator.
                    return cls.stream(response, result)

                else:
                    # Leave it up to the response to throw or write whatever
                    # we got back.
                    response.end(result)
                    if response.body:
                        # Return the body if there was any set.
                        return response.body

        except http.exceptions.BaseHTTPException as e:
            # Something that we can handle and return properly happened.
            # Set response properties from the exception.
            response.status = e.status
            response.headers.update(e.headers)

            if e.content:
                # Write the exception body if present and close
                # the response.
                # TODO: Use the plain-text encoder.
                response.send(e.content, serialize=True, format='json')

            # Terminate the connection and return the body.
            response.close()
            if response.body:
                return response.body

        except Exception:
            # Something unexpected happened.
            # Log error message to the logger.
            logger.exception('Internal server error')

            # Write a debug message for the client.
            if not response.streaming and not response.closed:
                response.status = http.client.INTERNAL_SERVER_ERROR
                response.headers.clear()
                response.close()