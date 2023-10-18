def raise_for_status(response):
    """Raise an appropriate error for a given response.

    Arguments:
      response (:py:class:`aiohttp.ClientResponse`): The API response.

    Raises:
      :py:class:`aiohttp.web_exceptions.HTTPException`: The appropriate
        error for the response's status.

    """
    for err_name in web_exceptions.__all__:
        err = getattr(web_exceptions, err_name)
        if err.status_code == response.status:
            payload = dict(
                headers=response.headers,
                reason=response.reason,
            )
            if issubclass(err, web_exceptions._HTTPMove):  # pylint: disable=protected-access
                raise err(response.headers['Location'], **payload)
            raise err(**payload)