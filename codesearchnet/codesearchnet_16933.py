def _extract_path_from_service(self, service):
        """
        Extract path object and its parameters from service definitions.

        :param service:
            Cornice service to extract information from.

        :rtype: dict
        :returns: Path definition.
        """

        path_obj = {}
        path = service.path
        route_name = getattr(service, 'pyramid_route', None)
        # handle services that don't create fresh routes,
        # we still need the paths so we need to grab pyramid introspector to
        # extract that information
        if route_name:
            # avoid failure if someone forgets to pass registry
            registry = self.pyramid_registry or get_current_registry()
            route_intr = registry.introspector.get('routes', route_name)
            if route_intr:
                path = route_intr['pattern']
            else:
                msg = 'Route `{}` is not found by ' \
                      'pyramid introspector'.format(route_name)
                raise ValueError(msg)

        # handle traverse and subpath as regular parameters
        # docs.pylonsproject.org/projects/pyramid/en/latest/narr/hybrid.html
        for subpath_marker in ('*subpath', '*traverse'):
            path = path.replace(subpath_marker, '{subpath}')

        # Extract path parameters
        parameters = self.parameters.from_path(path)
        if parameters:
            path_obj['parameters'] = parameters

        return path, path_obj