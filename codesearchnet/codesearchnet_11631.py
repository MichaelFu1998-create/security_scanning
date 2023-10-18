def getDependencies(self,
        available_components = None,
                 search_dirs = None,
                      target = None,
              available_only = False,
                        test = False,
                    warnings = True
        ):
        ''' Returns {component_name:component}
        '''
        if search_dirs is None:
            search_dirs = [self.modulesPath()]
        available_components = self.ensureOrderedDict(available_components)

        components, errors = self.__getDependenciesWithProvider(
            available_components = available_components,
                     search_dirs = search_dirs,
                          target = target,
                update_installed = False,
                        provider = self.provideInstalled,
                            test = test
        )
        if warnings:
            for error in errors:
                logger.warning(error)
        if available_only:
            components = OrderedDict((k, v) for k, v in components.items() if v)
        return components