def get_current_thumbprint(self, components=None):
        """
        Returns a dictionary representing the current configuration state.

        Thumbprint is of the form:

            {
                component_name1: {key: value},
                component_name2: {key: value},
                ...
            }

        """
        components = str_to_component_list(components)
        if self.verbose:
            print('deploy.get_current_thumbprint.components:', components)
        manifest_data = {} # {component:data}
        for component_name, func in sorted(manifest_recorder.items()):
            self.vprint('Checking thumbprint for component %s...' % component_name)
            manifest_key = assert_valid_satchel(component_name)
            service_name = clean_service_name(component_name)
            if service_name not in self.genv.services:
                self.vprint('Skipping unused component:', component_name)
                continue
            elif components and service_name not in components:
                self.vprint('Skipping non-matching component:', component_name)
                continue
            try:
                self.vprint('Retrieving manifest for %s...' % component_name)
                manifest_data[manifest_key] = func()
                if self.verbose:
                    pprint(manifest_data[manifest_key], indent=4)
            except exceptions.AbortDeployment as e:
                raise
        return manifest_data