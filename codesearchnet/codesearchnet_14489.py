def wait_for_requests(pbclient, request_ids=None,
                      timeout=0, initial_wait=5, scaleup=10):
    '''
    Waits for a list of requests to finish until timeout.
    timeout==0 is interpreted as infinite wait time.
    Returns a dict of request_id -> result.
    result is a tuple (return code, request status, message) where return code
    0  : request successful
    1  : request failed
    -1 : timeout exceeded
    The wait_period is increased every scaleup steps to adjust for long
    running requests.
    '''
    done = dict()
    if not request_ids:
        print("empty request list")
        return done
    total_wait = 0
    wait_period = initial_wait
    next_scaleup = scaleup * wait_period
    wait = True
    while wait:
        for request_id in request_ids:
            if request_id in done:
                continue
            request_status = pbclient.get_request(request_id, status=True)
            state = request_status['metadata']['status']
            if state == "DONE":
                done[request_id] = (0, state, request_status['metadata']['message'])
                print("Request '{}' is in state '{}'.".format(request_id, state))
            if state == 'FAILED':
                done[request_id] = (1, state, request_status['metadata']['message'])
                print("Request '{}' is in state '{}'.".format(request_id, state))
        # end for(request_ids)
        if len(done) == len(request_ids):
            wait = False
        else:
            print("{} of {} requests are finished. Sleeping for {} seconds..."
                  .format(len(done), len(request_ids), wait_period))
            sleep(wait_period)
            total_wait += wait_period
            if timeout != 0 and total_wait > timeout:
                wait = False
            next_scaleup -= wait_period
            if next_scaleup == 0:
                wait_period += initial_wait
                next_scaleup = scaleup * wait_period
                print("scaling up wait_period to {}, next change in {} seconds"
                      .format(wait_period, next_scaleup))
        # end if/else(done)
    # end while(wait)
    if len(done) != len(request_ids):
        for request_id in request_ids:
            if request_id in done:
                continue
            done[request_id] = (-1, state, "request not finished before timeout")
    return done