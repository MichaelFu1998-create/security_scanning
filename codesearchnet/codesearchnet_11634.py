def getDependenciesRecursive(self,
                 available_components = None,
                            processed = None,
                          search_dirs = None,
                               target = None,
                       available_only = False,
                                 test = False
        ):
        ''' Get available and already installed components, don't check for
            remotely available components. See also
            satisfyDependenciesRecursive()

            Returns {component_name:component}
        '''
        components, errors = self.__getDependenciesRecursiveWithProvider(
           available_components = available_components,
                    search_dirs = search_dirs,
                         target = target,
                 traverse_links = True,
               update_installed = False,
                       provider = self.provideInstalled,
                           test = test
        )
        for error in errors:
            logger.error(error)
        if available_only:
            components = OrderedDict((k, v) for k, v in components.items() if v)
        return components