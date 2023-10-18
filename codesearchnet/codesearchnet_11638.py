def getBinaries(self):
        ''' Return a dictionary of binaries to compile: {"dirname":"exename"},
            this is used when automatically generating CMakeLists

            Note that currently modules may define only a single executable
            binary or library to be built by the automatic build system, by
            specifying `"bin": "dir-to-be-built-into-binary"`, or `"lib":
            "dir-to-be-built-into-library"`, and the bin/lib will always have
            the same name as the module. The default behaviour if nothing is
            specified is for the 'source' directory to be built into a library.

            The module.json syntax may allow for other combinations in the
            future (and callers of this function should not rely on it
            returning only a single item). For example, a "bin": {"dirname":
            "exename"} syntax might be supported, however currently more
            complex builds must be controlled by custom CMakeLists.
        '''
        # the module.json syntax is a subset of the package.json syntax: a
        # single string that defines the source directory to use to build an
        # executable with the same name as the component. This may be extended
        # to include the rest of the npm syntax in future (map of source-dir to
        # exe name).
        if 'bin' in self.description:
            return {os.path.normpath(self.description['bin']): self.getName()}
        else:
            return {}