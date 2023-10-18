def __getDependenciesWithProvider(self,
                      available_components = None,
                               search_dirs = None,
                                    target = None,
                          update_installed = False,
                                  provider = None,
                                      test = False
   ):
        ''' Get installed components using "provider" to find (and possibly
            install) components.

            See documentation for __getDependenciesRecursiveWithProvider

            returns (components, errors)
        '''
        # sourceparse, , parse version source urls, internal
        from yotta.lib import sourceparse
        errors = []
        modules_path = self.modulesPath()
        def satisfyDep(dspec):
            try:
                r = provider(
                  dspec,
                  available_components,
                  search_dirs,
                  modules_path,
                  update_installed,
                  self
                )
                if r and not sourceparse.parseSourceURL(dspec.versionReq()).semanticSpecMatches(r.getVersion()):
                    shrinkwrap_msg = ''
                    if dspec.isShrinkwrapped():
                        shrinkwrap_msg = 'shrinkwrap on '
                    msg = 'does not meet specification %s required by %s%s' % (
                        dspec.versionReq(), shrinkwrap_msg, self.getName()
                    )
                    logger.debug('%s %s', r.getName(), msg)
                    r.setError(msg)
                return r
            except access_common.Unavailable as e:
                errors.append(e)
                self.dependencies_failed = True
            except vcs.VCSError as e:
                errors.append(e)
                self.dependencies_failed = True
        specs = self.getDependencySpecs(target=target)
        if not test:
            # filter out things that aren't test dependencies if necessary:
            specs = [x for x in specs if not x.is_test_dependency]
        #dependencies = pool.map(
        dependencies = map(
            satisfyDep, specs
        )
        self.installed_dependencies = True
        # stable order is important!
        return (OrderedDict([((d and d.getName()) or specs[i].name, d) for i, d in enumerate(dependencies)]), errors)