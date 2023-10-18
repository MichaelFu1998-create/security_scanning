async def read(response, loads=loads, encoding=None):
    """
        read the data of the response

    Parameters
    ----------
    response : aiohttp.ClientResponse
        response
    loads : callable
        json loads function
    encoding : :obj:`str`, optional
        character encoding of the response, if set to None
        aiohttp should guess the right encoding

    Returns
    -------
    :obj:`bytes`, :obj:`str`, :obj:`dict` or :obj:`list`
        the data returned depends on the response
    """
    ctype = response.headers.get('Content-Type', "").lower()

    try:
        if "application/json" in ctype:
            logger.info("decoding data as json")
            return await response.json(encoding=encoding, loads=loads)

        if "text" in ctype:
            logger.info("decoding data as text")
            return await response.text(encoding=encoding)

    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        data = await response.read()
        raise exceptions.PeonyDecodeError(response=response,
                                          data=data,
                                          exception=exc)

    return await response.read()