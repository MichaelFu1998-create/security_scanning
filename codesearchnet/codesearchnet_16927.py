def from_path(self, path):
        """
        Create a list of Swagger path params from a cornice service path.

        :type path: string
        :rtype: list
        """
        path_components = path.split('/')
        param_names = [comp[1:-1] for comp in path_components
                       if comp.startswith('{') and comp.endswith('}')]

        params = []
        for name in param_names:
            param_schema = colander.SchemaNode(colander.String(), name=name)
            param = self.parameter_converter('path', param_schema)
            if self.ref:
                param = self._ref(param)
            params.append(param)

        return params