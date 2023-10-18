def hasDependencyRecursively(self, name, target=None, test_dependencies=False):
        ''' Check if this module, or any of its dependencies, have a
            dependencies with the specified name in their dependencies, or in
            their targetDependencies corresponding to the specified target.

            Note that if recursive dependencies are not installed, this test
            may return a false-negative.
        '''
        # checking dependencies recursively isn't entirely straightforward, so
        # use the existing method to resolve them all before checking:
        dependencies = self.getDependenciesRecursive(
                               target = target,
                                 test = test_dependencies
        )
        return (name in dependencies)