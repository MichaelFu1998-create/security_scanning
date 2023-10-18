def launch_batch_workflow(self, batch_workflow):
        """Launches GBDX batch workflow.

        Args:
            batch_workflow (dict): Dictionary specifying batch workflow tasks.

        Returns:
            Batch Workflow id (str).
        """

        # hit workflow api
        url = '%(base_url)s/batch_workflows' % {
            'base_url': self.base_url
        }
        try:
            r = self.gbdx_connection.post(url, json=batch_workflow)
            batch_workflow_id = r.json()['batch_workflow_id']
            return batch_workflow_id
        except TypeError as e:
            self.logger.debug('Batch Workflow not launched, reason: {0}'.format(e))