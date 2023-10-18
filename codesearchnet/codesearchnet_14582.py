def wait_for_server(pbclient=None, dc_id=None, serverid=None,
                    indicator='state', state='AVAILABLE', timeout=300):
    '''
    wait for a server/VM to reach a defined state for a specified time
    indicator := {state|vmstate} specifies if server or VM stat is tested
    state specifies the status the indicator should have
    '''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc_id is None:
        raise ValueError("argument 'dc_id' must not be None")
    if serverid is None:
        raise ValueError("argument 'serverid' must not be None")
    total_sleep_time = 0
    seconds = 5
    while total_sleep_time < timeout:
        time.sleep(seconds)
        total_sleep_time += seconds
        if total_sleep_time == 60:
            # Increase polling interval after one minute
            seconds = 10
        elif total_sleep_time == 600:
            # Increase polling interval after 10 minutes
            seconds = 20
        server = getServerStates(pbclient, dc_id, serverid)
        if server[indicator] == state:
            break
    # end while(total_sleep_time)
    return server