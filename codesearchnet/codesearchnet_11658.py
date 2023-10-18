def build(self, builddir, component, args, release_build=False, build_args=None, targets=None,
              release_no_debug_info_build=False):
        ''' Execute the commands necessary to build this component, and all of
            its dependencies. '''
        if build_args is None:
            build_args = []
        if targets is None:
            targets = []
        # in the future this may be specified in the target description, but
        # for now we only support cmake, so everything is simple:
        if release_no_debug_info_build:
            build_type = 'Release'
        elif release_build:
            build_type = 'RelWithDebInfo'
        else:
            build_type = 'Debug'
        cmd = ['cmake', '-D', 'CMAKE_BUILD_TYPE=%s' % build_type, '-G', args.cmake_generator, '.']
        res = self.exec_helper(cmd, builddir)
        if res is not None:
            return res

        # work-around various yotta-specific issues with the generated
        # Ninja/project files:
        from yotta.lib import cmake_fixups
        cmake_fixups.applyFixupsForFenerator(args.cmake_generator, builddir, component)

        build_command = self.overrideBuildCommand(args.cmake_generator, targets=targets)
        if build_command:
            cmd = build_command + build_args
        else:
            cmd = ['cmake', '--build', builddir]
            if len(targets):
                # !!! FIXME: support multiple targets with the default CMake
                # build command
                cmd += ['--target', targets[0]]
            cmd += build_args
        res = self.exec_helper(cmd, builddir)
        if res is not None:
            return res
        hint = self.hintForCMakeGenerator(args.cmake_generator, component)
        if hint:
            logger.info(hint)