def wait_for_completion(self, response, timeout=3600, initial_wait=5, scaleup=10):
        """
        Poll resource request status until resource is provisioned.

        :param      response: A response dict, which needs to have a 'requestId' item.
        :type       response: ``dict``

        :param      timeout: Maximum waiting time in seconds. None means infinite waiting time.
        :type       timeout: ``int``

        :param      initial_wait: Initial polling interval in seconds.
        :type       initial_wait: ``int``

        :param      scaleup: Double polling interval every scaleup steps, which will be doubled.
        :type       scaleup: ``int``

        """
        if not response:
            return
        logger = logging.getLogger(__name__)
        wait_period = initial_wait
        next_increase = time.time() + wait_period * scaleup
        if timeout:
            timeout = time.time() + timeout
        while True:
            request = self.get_request(request_id=response['requestId'], status=True)

            if request['metadata']['status'] == 'DONE':
                break
            elif request['metadata']['status'] == 'FAILED':
                raise PBFailedRequest(
                    'Request {0} failed to complete: {1}'.format(
                        response['requestId'], request['metadata']['message']),
                    response['requestId']
                )

            current_time = time.time()
            if timeout and current_time > timeout:
                raise PBTimeoutError('Timed out waiting for request {0}.'.format(
                    response['requestId']), response['requestId'])

            if current_time > next_increase:
                wait_period *= 2
                next_increase = time.time() + wait_period * scaleup
                scaleup *= 2

            logger.info("Request %s is in state '%s'. Sleeping for %i seconds...",
                        response['requestId'], request['metadata']['status'], wait_period)
            time.sleep(wait_period)