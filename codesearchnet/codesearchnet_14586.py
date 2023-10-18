def wait_for_request(pbclient, request_id,
                     timeout=0, initial_wait=5, scaleup=10):
    '''
    Waits for a request to finish until timeout.
    timeout==0 is interpreted as infinite wait time.
    Returns a tuple (return code, request status, message) where return code
    0  : request successful
    1  : request failed
    -1 : timeout exceeded
    The wait_period is increased every scaleup steps to adjust for long
    running requests.
    '''
    total_wait = 0
    wait_period = initial_wait
    next_scaleup = scaleup * wait_period
    wait = True
    while wait:
        request_status = pbclient.get_request(request_id, status=True)
        state = request_status['metadata']['status']
        if state == "DONE":
            return(0, state, request_status['metadata']['message'])
        if state == 'FAILED':
            return(1, state, request_status['metadata']['message'])
        if verbose > 0:
            print("Request '{}' is in state '{}'. Sleeping for {} seconds..."
                  .format(request_id, state, wait_period))
        sleep(wait_period)
        total_wait += wait_period
        if timeout != 0 and total_wait > timeout:
            wait = False
        next_scaleup -= wait_period
        if next_scaleup == 0:
            wait_period += initial_wait
            next_scaleup = scaleup * wait_period
            if verbose > 0:
                print("scaling up wait_period to {}, next change in {} seconds"
                      .format(wait_period, next_scaleup))
    # end while(wait)
    return(-1, state, "request not finished before timeout")