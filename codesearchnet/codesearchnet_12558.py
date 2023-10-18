def batch_workflow_status(self, batch_workflow_id):
        """Checks GBDX batch workflow status.

         Args:
             batch workflow_id (str): Batch workflow id.

         Returns:
             Batch Workflow status (str).
        """
        self.logger.debug('Get status of batch workflow: ' + batch_workflow_id)
        url = '%(base_url)s/batch_workflows/%(batch_id)s' % {
            'base_url': self.base_url, 'batch_id': batch_workflow_id
        }
        r = self.gbdx_connection.get(url)

        return r.json()