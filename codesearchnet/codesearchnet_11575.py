def _validateListedSubdirsExist(self, component):
        ''' Return true if all the subdirectories which this component lists in
            its module.json file exist (although their validity is otherwise
            not checked).

            If they don't, warning messages are printed.
        '''
        lib_subdirs = component.getLibs(explicit_only=True)
        bin_subdirs = component.getBinaries()

        ok = True
        for d in lib_subdirs:
            if not os.path.exists(os.path.join(component.path, d)):
                logger.warning(
                    "lib directory \"%s\" doesn't exist but is listed in the module.json file of %s", d, component
                )
                ok = False

        for d in bin_subdirs:
            if not os.path.exists(os.path.join(component.path, d)):
                logger.warning(
                    "bin directory \"%s\" doesn't exist but is listed in the module.json file of %s", d, component
                )
                ok = False

        return ok