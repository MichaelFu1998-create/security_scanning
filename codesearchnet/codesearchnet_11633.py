def __getDependenciesRecursiveWithProvider(self,
                               available_components = None,
                                        search_dirs = None,
                                             target = None,
                                     traverse_links = False,
                                   update_installed = False,
                                           provider = None,
                                               test = False,
                                         _processed = None
    ):
        ''' Get installed components using "provider" to find (and possibly
            install) components.

            This function is called with different provider functions in order
            to retrieve a list of all of the dependencies, or install all
            dependencies.

            Returns
            =======
                (components, errors)

                components: dictionary of name:Component
                errors: sequence of errors

            Parameters
            ==========
                available_components:
                    None (default) or a dictionary of name:component. This is
                    searched before searching directories or fetching remote
                    components

                search_dirs:
                    None (default), or sequence of directories to search for
                    already installed, (but not yet loaded) components. Used so
                    that manually installed or linked components higher up the
                    dependency tree are found by their users lower down.

                    These directories are searched in order, and finally the
                    current directory is checked.

                target:
                    None (default), or a Target object. If specified the target
                    name and it's similarTo list will be used in resolving
                    dependencies. If None, then only target-independent
                    dependencies will be installed

                traverse_links:
                    False (default) or True: whether to recurse into linked
                    dependencies. You normally want to set this to "True" when
                    getting a list of dependencies, and False when installing
                    them (unless the user has explicitly asked dependencies to
                    be installed in linked components).

                provider: None (default) or function:
                          provider(
                            dependency_spec,
                            available_components,
                            search_dirs,
                            working_directory,
                            update_if_installed
                          )
                test:
                    True, False, 'toplevel': should test-only dependencies be
                    included (yes, no, or only at this level, not recursively)
        '''
        def recursionFilter(c):
            if not c:
                logger.debug('do not recurse into failed component')
                # don't recurse into failed components
                return False
            if c.getName() in _processed:
                logger.debug('do not recurse into already processed component: %s' % c)
                return False
            if c.installedLinked() and not traverse_links:
                return False
            return True
        available_components = self.ensureOrderedDict(available_components)
        if search_dirs is None:
            search_dirs = []
        if _processed is None:
            _processed = set()
        assert(test in [True, False, 'toplevel'])
        search_dirs.append(self.modulesPath())
        logger.debug('process %s\nsearch dirs:%s' % (self.getName(), search_dirs))
        if self.isTestDependency():
            logger.debug("won't provide test dependencies recursively for test dependency %s", self.getName())
            test = False
        components, errors = self.__getDependenciesWithProvider(
            available_components = available_components,
                     search_dirs = search_dirs,
                update_installed = update_installed,
                          target = target,
                        provider = provider,
                            test = test
        )
        _processed.add(self.getName())
        if errors:
            errors = ['Failed to satisfy dependencies of %s:' % self.path] + errors
        need_recursion = [x for x in filter(recursionFilter, components.values())]
        available_components.update(components)
        logger.debug('processed %s\nneed recursion: %s\navailable:%s\nsearch dirs:%s' % (self.getName(), need_recursion, available_components, search_dirs))
        if test == 'toplevel':
            test = False
        # NB: can't perform this step in parallel, since the available
        # components list must be updated in order
        for c in need_recursion:
            dep_components, dep_errors = c.__getDependenciesRecursiveWithProvider(
                available_components = available_components,
                         search_dirs = search_dirs,
                              target = target,
                      traverse_links = traverse_links,
                    update_installed = update_installed,
                            provider = provider,
                                test = test,
                          _processed = _processed
            )
            available_components.update(dep_components)
            components.update(dep_components)
            errors += dep_errors
        return (components, errors)