def generateRecursive(self, component, all_components, builddir=None, modbuilddir=None, processed_components=None, application=None):
        ''' generate top-level CMakeLists for this component and its
            dependencies: the CMakeLists are all generated in self.buildroot,
            which MUST be out-of-source

            !!! NOTE: experimenting with a slightly different way of doing
            things here, this function is a generator that yields any errors
            produced, so the correct use is:

            for error in gen.generateRecursive(...):
                print(error)
        '''
        assert(self.configured)

        if builddir is None:
            builddir = self.buildroot
        if modbuilddir is None:
            modbuilddir = os.path.join(builddir, 'ym')

        if processed_components is None:
            processed_components = dict()
        if not self.target:
            yield 'Target "%s" is not a valid build target' % self.target

        toplevel = not len(processed_components)

        logger.debug('generate build files: %s (target=%s)' % (component, self.target))
        # because of the way c-family language includes work we need to put the
        # public header directories of all components that this component
        # depends on (directly OR indirectly) into the search path, which means
        # we need to first enumerate all the direct and indirect dependencies
        recursive_deps = component.getDependenciesRecursive(
            available_components = all_components,
                          target = self.target,
                  available_only = True,
                            test = True
        )
        dependencies = component.getDependencies(
                  all_components,
                          target = self.target,
                  available_only = True,
                            test = True
        )

        for name, dep in dependencies.items():
            # if dep is a test dependency, then it might not be required (if
            # we're not building tests). We don't actually know at this point
            if not dep:
                if dep.isTestDependency():
                    logger.debug('Test dependency "%s" of "%s" is not installed.' % (name, component))
                else:
                    yield 'Required dependency "%s" of "%s" is not installed.' % (name, component)
        # ensure this component is assumed to have been installed before we
        # check for its dependencies, in case it has a circular dependency on
        # itself
        processed_components[component.getName()] = component
        new_dependencies = OrderedDict([(name,c) for name,c in dependencies.items() if c and not name in processed_components])
        self.generate(builddir, modbuilddir, component, new_dependencies, dependencies, recursive_deps, application, toplevel)

        logger.debug('recursive deps of %s:' % component)
        for d in recursive_deps.values():
            logger.debug('    %s' % d)

        processed_components.update(new_dependencies)
        for name, c in new_dependencies.items():
            for error in self.generateRecursive(
                c, all_components, os.path.join(modbuilddir, name), modbuilddir, processed_components, application=application
            ):
                yield error