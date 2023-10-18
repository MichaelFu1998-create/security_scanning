def cancel(self, workflow_id):
        """Cancels a running workflow.

           Args:
               workflow_id (str): Workflow id.

           Returns:
               Nothing
        """
        self.logger.debug('Canceling workflow: ' + workflow_id)
        url = '%(wf_url)s/%(wf_id)s/cancel' % {
            'wf_url': self.workflows_url, 'wf_id': workflow_id
        }
        r = self.gbdx_connection.post(url, data='')
        r.raise_for_status()