def hasDependency(self, name, target=None, test_dependencies=False):
        ''' Check if this module has any dependencies with the specified name
            in its dependencies list, or in target dependencies for the
            specified target
        '''
        if name in self.description.get('dependencies', {}).keys():
            return True

        target_deps = self.description.get('targetDependencies', {})
        if target is not None:
            for conf_key, target_conf_deps in target_deps.items():
                if _truthyConfValue(target.getConfigValue(conf_key)) or conf_key in target.getSimilarTo_Deprecated():
                    if name in target_conf_deps:
                        return True

        if test_dependencies:
            if name in self.description.get('testDependencies', {}).keys():
                return True

            if target is not None:
                test_target_deps = self.description.get('testTargetDependencies', {})
                for conf_key, target_conf_deps in test_target_deps.items():
                    if _truthyConfValue(target.getConfigValue(conf_key)) or conf_key in target.getSimilarTo_Deprecated():
                        if name in target_conf_deps:
                            return True
        return False