def lookup_stdout(self, pk=None, start_line=None, end_line=None,
                      full=True):
        """
        Internal method that lies to our `monitor` method by returning
        a scorecard for the workflow job where the standard out
        would have been expected.
        """
        uj_res = get_resource('unified_job')
        # Filters
        #  - limit search to jobs spawned as part of this workflow job
        #  - order in the order in which they should add to the list
        #  - only include final job states
        query_params = (('unified_job_node__workflow_job', pk),
                        ('order_by', 'finished'),
                        ('status__in', 'successful,failed,error'))
        jobs_list = uj_res.list(all_pages=True, query=query_params)
        if jobs_list['count'] == 0:
            return ''

        return_content = ResSubcommand(uj_res)._format_human(jobs_list)
        lines = return_content.split('\n')
        if not full:
            lines = lines[:-1]

        N = len(lines)
        start_range = start_line
        if start_line is None:
            start_range = 0
        elif start_line > N:
            start_range = N

        end_range = end_line
        if end_line is None or end_line > N:
            end_range = N

        lines = lines[start_range:end_range]
        return_content = '\n'.join(lines)
        if len(lines) > 0:
            return_content += '\n'

        return return_content