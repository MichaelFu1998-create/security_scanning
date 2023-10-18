def getDependencySpecs(self, target=None):
        ''' Returns [DependencySpec]

            These are returned in the order that they are listed in the
            component description file: this is so that dependency resolution
            proceeds in a predictable way.
        '''
        deps = []

        def specForDependency(name, version_spec, istest):
            shrinkwrap = self.getShrinkwrapMapping()
            shrinkwrap_version_req = None
            if name in shrinkwrap:
                # exact version, and pull from registry:
                shrinkwrap_version_req = shrinkwrap[name]
                logger.debug(
                    'respecting %s shrinkwrap version %s for %s', self.getName(), shrinkwrap_version_req, name
                )
            return pack.DependencySpec(
                                         name,
                                         version_spec,
                                         istest,
                shrinkwrap_version_req = shrinkwrap_version_req,
                     specifying_module = self.getName()
            )

        deps += [specForDependency(x[0], x[1], False) for x in self.description.get('dependencies', {}).items()]
        target_deps = self.description.get('targetDependencies', {})
        if target is not None:
            for conf_key, target_conf_deps in target_deps.items():
                if _truthyConfValue(target.getConfigValue(conf_key)) or conf_key in target.getSimilarTo_Deprecated():
                    logger.debug(
                        'Adding target-dependent dependency specs for target config %s to component %s' %
                        (conf_key, self.getName())
                    )
                    deps += [specForDependency(x[0], x[1], False) for x in target_conf_deps.items()]


        deps += [specForDependency(x[0], x[1], True) for x in self.description.get('testDependencies', {}).items()]
        target_deps = self.description.get('testTargetDependencies', {})
        if target is not None:
            for conf_key, target_conf_deps in target_deps.items():
                if _truthyConfValue(target.getConfigValue(conf_key)) or conf_key in target.getSimilarTo_Deprecated():
                    logger.debug(
                        'Adding test-target-dependent dependency specs for target config %s to component %s' %
                        (conf_key, self.getName())
                    )
                    deps += [specForDependency(x[0], x[1], True) for x in target_conf_deps.items()]

        # remove duplicates (use the first occurrence)
        seen = set()
        r = []
        for dep in deps:
            if not dep.name in seen:
                r.append(dep)
                seen.add(dep.name)

        return r