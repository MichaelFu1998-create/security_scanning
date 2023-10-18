def _get_schema(self, wfjt_id):
        """
        Returns a dictionary that represents the node network of the
        workflow job template
        """
        node_res = get_resource('node')
        node_results = node_res.list(workflow_job_template=wfjt_id,
                                     all_pages=True)['results']
        return self._workflow_node_structure(node_results)