def schema(self, wfjt, node_network=None):
        """
        Convert YAML/JSON content into workflow node objects if
        node_network param is given.
        If not, print a YAML representation of the node network.

        =====API DOCS=====
        Convert YAML/JSON content into workflow node objects if ``node_network`` param is given. If not,
        print a YAML representation of the node network.

        :param wfjt: Primary key or name of the workflow job template to run schema against.
        :type wfjt: str
        :param node_network: JSON- or YAML-formatted string representing the topology of the workflow job
                             template be updated to.
        :type node_network: str
        :returns: The latest topology (possibly after modification) of the workflow job template.
        :rtype: dict

        =====API DOCS=====
        """
        existing_network = self._get_schema(wfjt)
        if not isinstance(existing_network, list):
            existing_network = []
        if node_network is None:
            if settings.format == 'human':
                settings.format = 'yaml'
            return existing_network

        if hasattr(node_network, 'read'):
            node_network = node_network.read()
        node_network = string_to_dict(
            node_network, allow_kv=False, require_dict=False)
        if not isinstance(node_network, list):
            node_network = []

        _update_workflow([TreeNode(x, wfjt, include_id=True) for x in existing_network],
                         [TreeNode(x, wfjt) for x in node_network])

        if settings.format == 'human':
            settings.format = 'yaml'
        return self._get_schema(wfjt)