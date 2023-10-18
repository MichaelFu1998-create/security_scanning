def launch(self, workflow):
        """Launches GBDX workflow.

        Args:
            workflow (dict): Dictionary specifying workflow tasks.

        Returns:
            Workflow id (str).
        """

        # hit workflow api
        try:
            r = self.gbdx_connection.post(self.workflows_url, json=workflow)
            try:
                r.raise_for_status()
            except:
                print("GBDX API Status Code: %s" % r.status_code)
                print("GBDX API Response: %s" % r.text)
                r.raise_for_status()
            workflow_id = r.json()['id']
            return workflow_id
        except TypeError:
            self.logger.debug('Workflow not launched!')