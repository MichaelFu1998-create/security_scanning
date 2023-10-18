def stdout(self, pk, start_line=None, end_line=None, outfile=sys.stdout, **kwargs):
        """
        Print out the standard out of a unified job to the command line or output file.
        For Projects, print the standard out of most recent update.
        For Inventory Sources, print standard out of most recent sync.
        For Jobs, print the job's standard out.
        For Workflow Jobs, print a status table of its jobs.

        =====API DOCS=====
        Print out the standard out of a unified job to the command line or output file.
        For Projects, print the standard out of most recent update.
        For Inventory Sources, print standard out of most recent sync.
        For Jobs, print the job's standard out.
        For Workflow Jobs, print a status table of its jobs.

        :param pk: Primary key of the job resource object to be monitored.
        :type pk: int
        :param start_line: Line at which to start printing job output
        :param end_line: Line at which to end printing job output
        :param outfile: Alternative file than stdout to write job stdout to.
        :type outfile: file
        :param `**kwargs`: Keyword arguments used to look up job resource object to monitor if ``pk`` is
                           not provided.
        :returns: A dictionary containing changed=False
        :rtype: dict

        =====API DOCS=====
        """

        # resource is Unified Job Template
        if self.unified_job_type != self.endpoint:
            unified_job = self.last_job_data(pk, **kwargs)
            pk = unified_job['id']
        # resource is Unified Job, but pk not given
        elif not pk:
            unified_job = self.get(**kwargs)
            pk = unified_job['id']

        content = self.lookup_stdout(pk, start_line, end_line)
        opened = False
        if isinstance(outfile, six.string_types):
            outfile = open(outfile, 'w')
            opened = True
        if len(content) > 0:
            click.echo(content, nl=1, file=outfile)
        if opened:
            outfile.close()

        return {"changed": False}