def generate(
            self, builddir, modbuilddir, component, active_dependencies, immediate_dependencies, all_dependencies, application, toplevel
        ):
        ''' active_dependencies is the dictionary of components that need to be
            built for this component, but will not already have been built for
            another component.
        '''

        include_root_dirs = ''
        if application is not None and component is not application:
            include_root_dirs += 'include_directories("%s")\n' % replaceBackslashes(application.path)

        include_sys_dirs = ''
        include_other_dirs = ''
        for name, c in itertools.chain(((component.getName(), component),), all_dependencies.items()):
            if c is not component and c.isTestDependency():
                continue
            include_root_dirs += 'include_directories("%s")\n' % replaceBackslashes(c.path)
            dep_sys_include_dirs = c.getExtraSysIncludes()
            for d in dep_sys_include_dirs:
                include_sys_dirs += 'include_directories(SYSTEM "%s")\n' % replaceBackslashes(os.path.join(c.path, d))
            dep_extra_include_dirs = c.getExtraIncludes()
            for d in dep_extra_include_dirs:
                include_other_dirs += 'include_directories("%s")\n' % replaceBackslashes(os.path.join(c.path, d))

        add_depend_subdirs = ''
        for name, c in active_dependencies.items():
            depend_subdir = replaceBackslashes(os.path.join(modbuilddir, name))
            relpath = replaceBackslashes(os.path.relpath(depend_subdir, self.buildroot))
            add_depend_subdirs += \
                'add_subdirectory(\n' \
                '   "%s"\n' \
                '   "${CMAKE_BINARY_DIR}/%s"\n' \
                ')\n' \
                % (depend_subdir, relpath)

        delegate_to_existing = None
        delegate_build_dir = None

        module_is_empty = False
        if os.path.isfile(os.path.join(component.path, 'CMakeLists.txt')) and not component.ignores('CMakeLists.txt'):
            # adding custom CMake is a promise to generate a library: so the
            # module is never empty in this case.
            delegate_to_existing = component.path
            add_own_subdirs = []
            logger.debug("delegate to build dir: %s", builddir)
            delegate_build_dir = os.path.join(builddir, 'existing')
        else:
            # !!! TODO: if they don't exist, that should possibly be a fatal
            # error, not just a warning
            self._validateListedSubdirsExist(component)

            subdirs = self._listSubDirectories(component, toplevel)
            manual_subdirs      = subdirs['manual']
            autogen_subdirs     = subdirs['auto']
            binary_subdirs      = subdirs['bin']
            lib_subdirs         = subdirs['lib']
            test_subdirs        = subdirs['test']
            resource_subdirs    = subdirs['resource']
            header_subdirs      = subdirs['headers']
            logger.debug("%s lib subdirs: %s, bin subdirs: %s", component, lib_subdirs, binary_subdirs)

            add_own_subdirs = []
            for f in manual_subdirs:
                if os.path.isfile(os.path.join(component.path, f, 'CMakeLists.txt')):
                    # if this module is a test dependency, then don't recurse
                    # to building its own tests.
                    if f in test_subdirs and component.isTestDependency():
                        continue
                    add_own_subdirs.append(
                        (os.path.join(component.path, f), f)
                    )
            # names of all directories at this level with stuff in: used to figure
            # out what to link automatically
            all_subdirs = manual_subdirs + [x[0] for x in autogen_subdirs]

            # first check if this module is empty:
            if component.isTestDependency():
                if len(autogen_subdirs) + len(add_own_subdirs) == 0:
                    module_is_empty = True
            else:
                if len(autogen_subdirs) + len(add_own_subdirs) <= len(test_subdirs):
                    module_is_empty = True

            # autogenerate CMakeLists for subdirectories as appropriate:
            for f, source_files in autogen_subdirs:
                if f in test_subdirs:
                    # if this module is a test dependency, then don't recurse
                    # to building its own tests.
                    if component.isTestDependency():
                        continue
                    self.generateTestDirList(
                        builddir, f, source_files, component, immediate_dependencies, toplevel=toplevel, module_is_empty=module_is_empty
                    )
                else:
                    if f in binary_subdirs:
                        is_executable = True
                        object_name = binary_subdirs[f]
                    else:
                        # not a test subdir or binary subdir: it must be a lib
                        # subdir
                        assert(f in lib_subdirs)
                        object_name = lib_subdirs[f]

                    for header_dir, header_files in header_subdirs:
                        source_files.extend(header_files)

                    self.generateSubDirList(
                                      builddir = builddir,
                                       dirname = f,
                                  source_files = source_files,
                                     component = component,
                                   all_subdirs = all_subdirs,
                        immediate_dependencies = immediate_dependencies,
                                   object_name = object_name,
                              resource_subdirs = resource_subdirs,
                                 is_executable = (f in binary_subdirs)
                    )
                add_own_subdirs.append(
                    (os.path.join(builddir, f), f)
                )

            # from now on, completely forget that this component had any tests
            # if it is itself a test dependency:
            if component.isTestDependency():
                test_subdirs = []

            # if we're not building anything other than tests, and this is a
            # library module (not a binary) then we need to generate a dummy
            # library so that this component can still be linked against
            if module_is_empty:
                if len(binary_subdirs):
                    logger.warning('nothing to build!')
                else:
                    add_own_subdirs.append(self.createDummyLib(
                        component, builddir, [x[0] for x in immediate_dependencies.items() if not x[1].isTestDependency()]
                    ))

        toolchain_file_path = os.path.join(builddir, 'toolchain.cmake')
        if toplevel:
            # generate the top-level toolchain file:
            template = jinja_environment.get_template('toolchain.cmake')
            file_contents = template.render({  #pylint: disable=no-member
                                   # toolchain files are provided in hierarchy
                                   # order, but the template needs them in reverse
                                   # order (base-first):
                "toolchain_files": self.target.getToolchainFiles()
            })
            self._writeFile(toolchain_file_path, file_contents)

        # generate the top-level CMakeLists.txt
        template = jinja_environment.get_template('base_CMakeLists.txt')

        relpath = os.path.relpath(builddir, self.buildroot)

        file_contents = template.render({ #pylint: disable=no-member
                            "toplevel": toplevel,
                         "target_name": self.target.getName(),
                     "set_definitions": self.set_toplevel_definitions,
                      "toolchain_file": toolchain_file_path,
                           "component": component,
                             "relpath": relpath,
                   "include_root_dirs": include_root_dirs,
                    "include_sys_dirs": include_sys_dirs,
                  "include_other_dirs": include_other_dirs,
                  "add_depend_subdirs": add_depend_subdirs,
                     "add_own_subdirs": add_own_subdirs,
                 "config_include_file": self.config_include_file,
                         "delegate_to": delegate_to_existing,
                  "delegate_build_dir": delegate_build_dir,
                 "active_dependencies": active_dependencies,
                     "module_is_empty": module_is_empty,
                      "cmake_includes": self.target.getAdditionalIncludes()
        })
        self._writeFile(os.path.join(builddir, 'CMakeLists.txt'), file_contents)