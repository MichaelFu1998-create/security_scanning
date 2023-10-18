def check_for_rate_limiting(response, response_lambda, timeout=1, attempts=0):
    """
    Takes an initial response, and a way to repeat the request that produced it and retries the request with an increasing sleep period between requests if rate limiting resposne codes are encountered.

    If more than 3 attempts are made, a RateLimitingException is raised

    :param response: A response from Citrination
    :type response: requests.Response
    :param response_lambda: a callable that runs the request that returned the
        response
    :type response_lambda: function
    :param timeout: the time to wait before retrying
    :type timeout: int
    :param attempts: the number of the retry being executed
    :type attempts: int
    """
    if attempts >= 3:
        raise RateLimitingException()
    if response.status_code == 429:
        sleep(timeout)
        new_timeout = timeout + 1
        new_attempts = attempts + 1
        return check_for_rate_limiting(response_lambda(timeout, attempts), response_lambda, timeout=new_timeout, attempts=new_attempts)
    return response