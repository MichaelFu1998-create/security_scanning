def wait_for_datacenter(client, data_center_id):
    '''
    Poll the data center to become available (for the next provisionig job)
    '''
    total_sleep_time = 0
    seconds = 5
    while True:
        state = client.get_datacenter(data_center_id)['metadata']['state']
        if verbose:
            print("datacenter is {}".format(state))
        if state == "AVAILABLE":
            break
        time.sleep(seconds)
        total_sleep_time += seconds
        if total_sleep_time == 60:
            # Increase polling interval after one minute
            seconds = 10
        elif total_sleep_time == 600:
            # Increase polling interval after 10 minutes
            seconds = 20