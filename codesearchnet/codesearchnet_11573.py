def configure(self, component, all_dependencies):
        ''' Ensure all config-time files have been generated. Return a
            dictionary of generated items.
        '''
        r = {}

        builddir = self.buildroot

        # only dependencies which are actually valid can contribute to the
        # config data (which includes the versions of all dependencies in its
        # build info) if the dependencies aren't available we can't tell what
        # version they are. Anything missing here should always be a test
        # dependency that isn't going to be used, otherwise the yotta build
        # command will fail before we get here
        available_dependencies = OrderedDict((k, v) for k, v in all_dependencies.items() if v)

        self.set_toplevel_definitions = ''
        if self.build_info_include_file is None:
            self.build_info_include_file, build_info_definitions = self.getBuildInfo(component.path, builddir)
            self.set_toplevel_definitions += build_info_definitions

        if self.config_include_file is None:
            self.config_include_file, config_definitions, self.config_json_file = self._getConfigData(available_dependencies, component, builddir, self.build_info_include_file)
            self.set_toplevel_definitions += config_definitions

        self.configured = True
        return {
            'merged_config_include': self.config_include_file,
               'merged_config_json': self.config_json_file,
               'build_info_include': self.build_info_include_file
        }