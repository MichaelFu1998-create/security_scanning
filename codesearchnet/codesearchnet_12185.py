def shutdown_check_handler():
    """This checks the AWS instance data URL to see if there's a pending
    shutdown for the instance.

    This is useful for AWS spot instances. If there is a pending shutdown posted
    to the instance data URL, we'll use the result of this function break out of
    the processing loop and shut everything down ASAP before the instance dies.

    Returns
    -------

    bool
        - True if the instance is going to die soon.
        - False if the instance is still safe.

    """

    url = 'http://169.254.169.254/latest/meta-data/spot/instance-action'

    try:
        resp = requests.get(url, timeout=1.0)
        resp.raise_for_status()

        stopinfo = resp.json()
        if 'action' in stopinfo and stopinfo['action'] in ('stop',
                                                           'terminate',
                                                           'hibernate'):
            stoptime = stopinfo['time']
            LOGWARNING('instance is going to %s at %s' % (stopinfo['action'],
                                                          stoptime))

            resp.close()
            return True
        else:
            resp.close()
            return False

    except HTTPError as e:
        resp.close()
        return False

    except Exception as e:
        resp.close()
        return False