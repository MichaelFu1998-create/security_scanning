def batch_workflow_cancel(self, batch_workflow_id):
        """Cancels GBDX batch workflow.

         Args:
             batch workflow_id (str): Batch workflow id.

         Returns:
             Batch Workflow status (str).
        """
        self.logger.debug('Cancel batch workflow: ' + batch_workflow_id)
        url = '%(base_url)s/batch_workflows/%(batch_id)s/cancel' % {
            'base_url': self.base_url, 'batch_id': batch_workflow_id
        }
        r = self.gbdx_connection.post(url)

        return r.json()