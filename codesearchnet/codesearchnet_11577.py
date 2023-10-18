def _getConfigData(self, all_dependencies, component, builddir, build_info_header_path):
        ''' returns (path_to_config_header, cmake_set_definitions) '''
        # ordered_json, , read/write ordered json, internal
        from yotta.lib import ordered_json
        add_defs_header = ''
        set_definitions = ''
        # !!! backwards-compatible "TARGET_LIKE" definitions for the top-level
        # of the config. NB: THESE WILL GO AWAY
        definitions = []
        definitions.append(('TARGET', sanitizePreprocessorSymbol(self.target.getName())))
        definitions.append(('TARGET_LIKE_%s' % sanitizePreprocessorSymbol(self.target.getName()),None))

        # make the path to the build-info header available both to CMake and
        # in the preprocessor:
        full_build_info_header_path = replaceBackslashes(os.path.abspath(build_info_header_path))
        logger.debug('build info header include path: "%s"', full_build_info_header_path)
        definitions.append(('YOTTA_BUILD_INFO_HEADER', '"'+full_build_info_header_path+'"'))

        for target in self.target.getSimilarTo_Deprecated():
            if '*' not in target:
                definitions.append(('TARGET_LIKE_%s' % sanitizePreprocessorSymbol(target),None))

        merged_config = self.target.getMergedConfig()
        logger.debug('target configuration data: %s', merged_config)
        definitions += self._definitionsForConfig(merged_config, ['YOTTA', 'CFG'])

        add_defs_header += '// yotta config data (including backwards-compatible definitions)\n'

        for k, v in definitions:
            if v is not None:
                add_defs_header += '#define %s %s\n' % (k, v)
                set_definitions += 'set(%s %s)\n' % (k, v)
            else:
                add_defs_header += '#define %s\n' % k
                set_definitions += 'set(%s TRUE)\n' % k

        add_defs_header += '\n// version definitions\n'

        for dep in list(all_dependencies.values()) + [component]:
            add_defs_header += "#define YOTTA_%s_VERSION_STRING \"%s\"\n" % (sanitizePreprocessorSymbol(dep.getName()), str(dep.getVersion()))
            add_defs_header += "#define YOTTA_%s_VERSION_MAJOR %d\n" % (sanitizePreprocessorSymbol(dep.getName()), dep.getVersion().major())
            add_defs_header += "#define YOTTA_%s_VERSION_MINOR %d\n" % (sanitizePreprocessorSymbol(dep.getName()), dep.getVersion().minor())
            add_defs_header += "#define YOTTA_%s_VERSION_PATCH %d\n" % (sanitizePreprocessorSymbol(dep.getName()), dep.getVersion().patch())

        # add the component's definitions
        defines = component.getDefines()
        if defines:
            add_defs_header += "\n// direct definitions (defines.json)\n"
            for name, value in defines.items():
                add_defs_header += "#define %s %s\n" % (name, value)
            add_defs_header += '\n'

        # use -include <definitions header> instead of lots of separate
        # defines... this is compiler specific, but currently testing it
        # out for gcc-compatible compilers only:
        config_include_file = os.path.join(builddir, 'yotta_config.h')
        config_json_file    = os.path.join(builddir, 'yotta_config.json')
        set_definitions += 'set(YOTTA_CONFIG_MERGED_JSON_FILE \"%s\")\n' % replaceBackslashes(os.path.abspath(config_json_file))

        self._writeFile(
            config_include_file,
            '#ifndef __YOTTA_CONFIG_H__\n'+
            '#define __YOTTA_CONFIG_H__\n'+
            add_defs_header+
            '#endif // ndef __YOTTA_CONFIG_H__\n'
        )
        self._writeFile(
            config_json_file,
            ordered_json.dumps(merged_config)
        )
        return (config_include_file, set_definitions, config_json_file)