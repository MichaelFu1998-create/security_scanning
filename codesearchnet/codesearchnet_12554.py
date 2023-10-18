def status(self, workflow_id):
        """Checks workflow status.

         Args:
             workflow_id (str): Workflow id.

         Returns:
             Workflow status (str).
        """
        self.logger.debug('Get status of workflow: ' + workflow_id)
        url = '%(wf_url)s/%(wf_id)s' % {
            'wf_url': self.workflows_url, 'wf_id': workflow_id
        }
        r = self.gbdx_connection.get(url)
        r.raise_for_status()
        return r.json()['state']