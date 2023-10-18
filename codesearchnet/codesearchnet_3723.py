def wait(self, pk, parent_pk=None, min_interval=1, max_interval=30, timeout=None, outfile=sys.stdout,
             exit_on=['successful'], **kwargs):
        """
        Wait for a running job to finish. Blocks further input until the job completes (whether successfully
        or unsuccessfully) and a final status can be given.

        =====API DOCS=====
        Wait for a job resource object to enter certain status.

        :param pk: Primary key of the job resource object to wait.
        :type pk: int
        :param parent_pk: Primary key of the unified job template resource object whose latest job run will be
                          waited if ``pk`` is not set.
        :type parent_pk: int
        :param timeout: Number in seconds after which this method will time out.
        :type timeout: float
        :param min_interval: Minimum polling interval to request an update from Tower.
        :type min_interval: float
        :param max_interval: Maximum polling interval to request an update from Tower.
        :type max_interval: float
        :param outfile: Alternative file than stdout to write job status updates on.
        :type outfile: file
        :param exit_on: Job resource object statuses to wait on.
        :type exit_on: array
        :param `**kwargs`: Keyword arguments used to look up job resource object to wait if ``pk`` is
                           not provided.
        :returns: A dictionary combining the JSON output of the status-changed job resource object, as well
                  as two extra fields: "changed", a flag indicating if the job resource object is status-changed
                  as expected; "id", an integer which is the primary key of the job resource object being
                  status-changed.
        :rtype: dict
        :raises tower_cli.exceptions.Timeout: When wait time reaches time out.
        :raises tower_cli.exceptions.JobFailure: When the job being waited on runs into failure.
        =====API DOCS=====
        """
        # If we do not have the unified job info, infer it from parent
        if pk is None:
            pk = self.last_job_data(parent_pk, **kwargs)['id']
        job_endpoint = '%s%s/' % (self.unified_job_type, pk)

        dots = itertools.cycle([0, 1, 2, 3])
        longest_string = 0
        interval = min_interval
        start = time.time()

        # Poll the Ansible Tower instance for status, and print the status to the outfile (usually standard out).
        #
        # Note that this is one of the few places where we use `secho` even though we're in a function that might
        # theoretically be imported and run in Python.  This seems fine; outfile can be set to /dev/null and very
        # much the normal use for this method should be CLI monitoring.
        result = client.get(job_endpoint).json()
        last_poll = time.time()
        timeout_check = 0
        while result['status'] not in exit_on:
            # If the job has failed, we want to raise an Exception for that so we get a non-zero response.
            if result['failed']:
                if is_tty(outfile) and not settings.verbose:
                    secho('\r' + ' ' * longest_string + '\n', file=outfile)
                raise exc.JobFailure('Job failed.')

            # Sanity check: Have we officially timed out?
            # The timeout check is incremented below, so this is checking to see if we were timed out as of
            # the previous iteration. If we are timed out, abort.
            if timeout and timeout_check - start > timeout:
                raise exc.Timeout('Monitoring aborted due to timeout.')

            # If the outfile is a TTY, print the current status.
            output = '\rCurrent status: %s%s' % (result['status'], '.' * next(dots))
            if longest_string > len(output):
                output += ' ' * (longest_string - len(output))
            else:
                longest_string = len(output)
            if is_tty(outfile) and not settings.verbose:
                secho(output, nl=False, file=outfile)

            # Put the process to sleep briefly.
            time.sleep(0.2)

            # Sanity check: Have we reached our timeout?
            # If we're about to time out, then we need to ensure that we do one last check.
            #
            # Note that the actual timeout will be performed at the start of the **next** iteration,
            # so there's a chance for the job's completion to be noted first.
            timeout_check = time.time()
            if timeout and timeout_check - start > timeout:
                last_poll -= interval

            # If enough time has elapsed, ask the server for a new status.
            #
            # Note that this doesn't actually do a status check every single time; we want the "spinner" to
            # spin even if we're not actively doing a check.
            #
            # So, what happens is that we are "counting down" (actually up) to the next time that we intend
            # to do a check, and once that time hits, we do the status check as part of the normal cycle.
            if time.time() - last_poll > interval:
                result = client.get(job_endpoint).json()
                last_poll = time.time()
                interval = min(interval * 1.5, max_interval)

                # If the outfile is *not* a TTY, print a status update when and only when we make an actual
                # check to job status.
                if not is_tty(outfile) or settings.verbose:
                    click.echo('Current status: %s' % result['status'], file=outfile)

            # Wipe out the previous output
            if is_tty(outfile) and not settings.verbose:
                secho('\r' + ' ' * longest_string, file=outfile, nl=False)
                secho('\r', file=outfile, nl=False)

        # Return the job ID and other response data
        answer = OrderedDict((('changed', True), ('id', pk)))
        answer.update(result)
        # Make sure to return ID of resource and not update number relevant for project creation and update
        if parent_pk:
            answer['id'] = parent_pk
        else:
            answer['id'] = pk
        return answer