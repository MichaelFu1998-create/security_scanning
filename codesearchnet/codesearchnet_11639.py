def getLibs(self, explicit_only=False):
        ''' Return a dictionary of libraries to compile: {"dirname":"libname"},
            this is used when automatically generating CMakeLists.

            If explicit_only is not set, then in the absence of both 'lib' and
            'bin' sections in the module.json file, the "source" directory
            will be returned.

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
        if 'lib' in self.description:
            return {os.path.normpath(self.description['lib']): self.getName()}
        elif 'bin' not in self.description and not explicit_only:
            return {'source': self.getName()}
        else:
            return {}