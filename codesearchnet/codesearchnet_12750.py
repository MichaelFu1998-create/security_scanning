async def throw(response, loads=None, encoding=None, **kwargs):
    """ Get the response data if possible and raise an exception """
    if loads is None:
        loads = data_processing.loads

    data = await data_processing.read(response, loads=loads,
                                      encoding=encoding)

    error = get_error(data)
    if error is not None:
        exception = errors[error['code']]
        raise exception(response=response, error=error, data=data, **kwargs)

    if response.status in statuses:
        exception = statuses[response.status]
        raise exception(response=response, data=data, **kwargs)

    # raise PeonyException if no specific exception was found
    raise PeonyException(response=response, data=data, **kwargs)