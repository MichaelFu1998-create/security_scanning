def lookup_stdout(self, pk=None, start_line=None, end_line=None, full=True):
        """
        Internal utility function to return standard out. Requires the pk of a unified job.
        """
        stdout_url = '%s%s/stdout/' % (self.unified_job_type, pk)
        payload = {'format': 'json', 'content_encoding': 'base64', 'content_format': 'ansi'}
        if start_line:
            payload['start_line'] = start_line
        if end_line:
            payload['end_line'] = end_line
        debug.log('Requesting a copy of job standard output', header='details')
        resp = client.get(stdout_url, params=payload).json()
        content = b64decode(resp['content'])
        return content.decode('utf-8', 'replace')