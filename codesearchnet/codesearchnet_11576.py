def _listSubDirectories(self, component, toplevel):
        ''' return: {
                manual: [list of subdirectories with manual CMakeLists],
                  auto: [list of pairs: (subdirectories name to autogenerate, a list of source files in that dir)],
                   bin: {dictionary of subdirectory name to binary name},
                   lib: {dictionary of subdirectory name to binary name},
                  test: [list of directories that build tests],
              resource: [list of directories that contain resources]
            }
        '''
        manual_subdirs = []
        auto_subdirs = []
        header_subdirs = []
        lib_subdirs = component.getLibs()
        bin_subdirs = component.getBinaries()
        test_subdirs = []
        resource_subdirs = []
        # if the application or library is set to get the sources from top level ("."),
        # they'll be acumulated into a single array (top_sources below).
        top_sources = []
        start_on_top = "." in [os.path.normpath(x) for x in list(lib_subdirs.keys()) + list(bin_subdirs.keys())]
        for f in sorted(os.listdir(component.path)):
            if f in Ignore_Subdirs or f.startswith('.') or f.startswith('_'):
                continue
            check_cmakefile_path = os.path.join(f, 'CMakeLists.txt')
            if os.path.isfile(os.path.join(component.path, check_cmakefile_path)) and not \
                    component.ignores(check_cmakefile_path):
                self.checkStandardSourceDir(f, component)
                # if the subdirectory has a CMakeLists.txt in it (and it isn't
                # ignored), then delegate to that:
                manual_subdirs.append(f)
                # tests only supported in the `test` directory for now
                if f in ('test',):
                    test_subdirs.append(f)
            else:
                if os.path.isfile(os.path.join(component.path, f)):
                    # top level source: check if it should be included
                    if not component.ignores(f) and start_on_top:
                        sf = self.createSourceFile(f, os.path.join(component.path, f), ".")
                        if sf is not None:
                            top_sources.append(sf)
                else:
                    # otherwise, if the directory has source files, and is listed
                    # as a source/test directory, generate a CMakeLists in the
                    # corresponding temporary directory, and add that.
                    sources = self.containsSourceFiles(os.path.join(component.path, f), component)
                    if sources:
                        if f in ('test',):
                            auto_subdirs.append((f, sources))
                            test_subdirs.append(f)
                        elif start_on_top:
                            # include the sources in this directory only if it's not
                            # a potential test directory
                            from yotta.lib import validate
                            if not validate.isPotentialTestDir(f):
                                top_sources.extend(sources)
                                if f == component.getName():
                                    header_subdirs.append((f, sources))
                        elif os.path.normpath(f) in [fsutils.fullySplitPath(x)[0] for x in lib_subdirs] or \
                             os.path.normpath(f) in [fsutils.fullySplitPath(x)[0] for x in bin_subdirs]:
                            for full_subpath in list(lib_subdirs.keys()) + list(bin_subdirs.keys()):
                                if fsutils.fullySplitPath(full_subpath)[0] == os.path.normpath(f):
                                    # this might be a sub-sub directory, in which
                                    # case we need to re-calculate the sources just
                                    # for the part we care about:
                                    sources = self.containsSourceFiles(os.path.join(component.path, full_subpath), component)
                                    auto_subdirs.append((full_subpath, sources))
                        elif f == component.getName():
                            header_subdirs.append((f, sources))
                    elif toplevel and \
                         ((f in ('test',)) or \
                          (os.path.normpath(f) in lib_subdirs or start_on_top) or \
                          (os.path.normpath(f) in bin_subdirs or start_on_top) and not \
                          component.ignores(f)):
                        # (if there aren't any source files then do nothing)
                        # !!! FIXME: ensure this warning is covered in tests
                        logger.warning("subdirectory \"%s\" of %s was ignored because it doesn't appear to contain any source files", f, component)

            # 'resource' directory also has special meaning, but there's no
            # pattern for the files which might be in here:
            if f in ('resource',):
                resource_subdirs.append(os.path.join(component.path, f))

            # issue a warning if a differently cased or common misspelling of a
            # standard directory name was encountered:
            check_directory_name_cases = list(lib_subdirs.keys()) + list(bin_subdirs.keys()) + ['test', 'resource']
            if f.lower() in check_directory_name_cases + ['src'] and not \
               f in check_directory_name_cases and not \
               component.ignores(f):
                self.checkStandardSourceDir(f, component)
        if top_sources:
            # all the top level sources are grouped into a single cmake-generated directory
            # which is given the same name as the component
            auto_subdirs.append((component.getName(), top_sources))

        return {
            "manual": manual_subdirs,
              "auto": auto_subdirs,
           "headers": header_subdirs,
               "bin": {component.getName(): component.getName()} if (start_on_top and component.isApplication()) else bin_subdirs,
               "lib": {component.getName(): component.getName()} if (start_on_top and not component.isApplication()) else lib_subdirs,
              "test": test_subdirs,
          "resource": resource_subdirs
        }