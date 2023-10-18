def _parent_filter(self, parent, relationship, **kwargs):
        """
        Returns filtering parameters to limit a search to the children
        of a particular node by a particular relationship.
        """
        if parent is None or relationship is None:
            return {}
        parent_filter_kwargs = {}
        query_params = ((self._reverse_rel_name(relationship), parent),)
        parent_filter_kwargs['query'] = query_params
        if kwargs.get('workflow_job_template', None) is None:
            parent_data = self.read(pk=parent)['results'][0]
            parent_filter_kwargs['workflow_job_template'] = parent_data[
                'workflow_job_template']
        return parent_filter_kwargs