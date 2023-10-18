def monitor(self, pk, parent_pk=None, timeout=None, interval=0.5, outfile=sys.stdout, **kwargs):
        """
        Stream the standard output from a job, project update, or inventory udpate.

        =====API DOCS=====
        Stream the standard output from a job run to stdout.

        :param pk: Primary key of the job resource object to be monitored.
        :type pk: int
        :param parent_pk: Primary key of the unified job template resource object whose latest job run will be
                          monitored if ``pk`` is not set.
        :type parent_pk: int
        :param timeout: Number in seconds after which this method will time out.
        :type timeout: float
        :param interval: Polling interval to refresh content from Tower.
        :type interval: float
        :param outfile: Alternative file than stdout to write job stdout to.
        :type outfile: file
        :param `**kwargs`: Keyword arguments used to look up job resource object to monitor if ``pk`` is
                           not provided.
        :returns: A dictionary combining the JSON output of the finished job resource object, as well as
                  two extra fields: "changed", a flag indicating if the job resource object is finished
                  as expected; "id", an integer which is the primary key of the job resource object being
                  monitored.
        :rtype: dict
        :raises tower_cli.exceptions.Timeout: When monitor time reaches time out.
        :raises tower_cli.exceptions.JobFailure: When the job being monitored runs into failure.

        =====API DOCS=====
        """

        # If we do not have the unified job info, infer it from parent
        if pk is None:
            pk = self.last_job_data(parent_pk, **kwargs)['id']
        job_endpoint = '%s%s/' % (self.unified_job_type, pk)

        # Pause until job is in running state
        self.wait(pk, exit_on=['running', 'successful'], outfile=outfile)

        # Loop initialization
        start = time.time()
        start_line = 0
        result = client.get(job_endpoint).json()

        click.echo('\033[0;91m------Starting Standard Out Stream------\033[0m', nl=2, file=outfile)

        # Poll the Ansible Tower instance for status and content, and print standard out to the out file
        while not result['failed'] and result['status'] != 'successful':

            result = client.get(job_endpoint).json()

            # Put the process to sleep briefly.
            time.sleep(interval)

            # Make request to get standard out
            content = self.lookup_stdout(pk, start_line, full=False)

            # In the first moments of running the job, the standard out
            # may not be available yet
            if not content.startswith("Waiting for results"):
                line_count = len(content.splitlines())
                start_line += line_count
                click.echo(content, nl=0, file=outfile)

            if timeout and time.time() - start > timeout:
                raise exc.Timeout('Monitoring aborted due to timeout.')

        # Special final line for closure with workflow jobs
        if self.endpoint == '/workflow_jobs/':
            click.echo(self.lookup_stdout(pk, start_line, full=True), nl=1)

        click.echo('\033[0;91m------End of Standard Out Stream--------\033[0m', nl=2, file=outfile)

        if result['failed']:
            raise exc.JobFailure('Job failed.')

        # Return the job ID and other response data
        answer = OrderedDict((('changed', True), ('id', pk)))
        answer.update(result)
        # Make sure to return ID of resource and not update number relevant for project creation and update
        if parent_pk:
            answer['id'] = parent_pk
        else:
            answer['id'] = pk
        return answer