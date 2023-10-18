def satisfyDependenciesRecursive(
                            self,
            available_components = None,
                     search_dirs = None,
                update_installed = False,
                  traverse_links = False,
                          target = None,
                            test = False
        ):
        ''' Retrieve and install all the dependencies of this component and its
            dependencies, recursively, or satisfy them from a collection of
            available_components or from disk.

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

                update_installed:
                    False (default), True, or set(): whether to check the
                    available versions of installed components, and update if a
                    newer version is available. If this is a set(), only update
                    things in the specified set.

                traverse_links:
                    False (default) or True: whether to recurse into linked
                    dependencies when updating/installing.

                target:
                    None (default), or a Target object. If specified the target
                    name and it's similarTo list will be used in resolving
                    dependencies. If None, then only target-independent
                    dependencies will be installed

                test:
                    True, False, or 'toplevel: should test-only dependencies be
                    installed? (yes, no, or only for this module, not its
                    dependencies).

        '''
        def provider(
            dspec,
            available_components,
            search_dirs,
            working_directory,
            update_installed,
            dep_of=None
        ):
            r = access.satisfyFromAvailable(dspec.name, available_components)
            if r:
                if r.isTestDependency() and not dspec.is_test_dependency:
                    logger.debug('test dependency subsequently occurred as real dependency: %s', r.getName())
                    r.setTestDependency(False)
                return r
            update_if_installed = False
            if update_installed is True:
                update_if_installed = True
            elif update_installed:
                update_if_installed = dspec.name in update_installed
            r = access.satisfyVersionFromSearchPaths(
                dspec.name,
                dspec.versionReq(),
                search_dirs,
                update_if_installed,
                inherit_shrinkwrap = dep_of.getShrinkwrap()
            )
            if r:
                r.setTestDependency(dspec.is_test_dependency)
                return r
            # before resorting to install this module, check if we have an
            # existing linked module (which wasn't picked up because it didn't
            # match the version specification) - if we do, then we shouldn't
            # try to install, but should return that anyway:
            default_path = os.path.join(self.modulesPath(), dspec.name)
            if fsutils.isLink(default_path):
                r = Component(
                                       default_path,
                     test_dependency = dspec.is_test_dependency,
                    installed_linked = fsutils.isLink(default_path),
                  inherit_shrinkwrap = dep_of.getShrinkwrap()
                )
                if r:
                    assert(r.installedLinked())
                    return r
                else:
                    logger.error('linked module %s is invalid: %s', dspec.name, r.getError())
                    return r

            r = access.satisfyVersionByInstalling(
                dspec.name,
                dspec.versionReq(),
                self.modulesPath(),
                inherit_shrinkwrap = dep_of.getShrinkwrap()
            )
            if not r:
                logger.error('could not install %s' % dspec.name)
            if r is not None:
                r.setTestDependency(dspec.is_test_dependency)
            return r

        return self.__getDependenciesRecursiveWithProvider(
           available_components = available_components,
                    search_dirs = search_dirs,
                         target = target,
                 traverse_links = traverse_links,
               update_installed = update_installed,
                       provider = provider,
                           test = test
        )