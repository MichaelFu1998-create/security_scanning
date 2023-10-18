def getBuildInfo(self, sourcedir, builddir):
        ''' Write the build info header file, and return (path_to_written_header, set_cmake_definitions) '''
        cmake_defs = ''
        preproc_defs = '// yotta build info, #include YOTTA_BUILD_INFO_HEADER to access\n'
        # standard library modules
        import datetime
        # vcs, , represent version controlled directories, internal
        from yotta.lib import vcs

        now = datetime.datetime.utcnow()
        vcs_instance = vcs.getVCS(sourcedir)
        if self.build_uuid is None:
            import uuid
            self.build_uuid = uuid.uuid4()

        definitions = [
            ('YOTTA_BUILD_YEAR',   now.year,        'UTC year'),
            ('YOTTA_BUILD_MONTH',  now.month,       'UTC month 1-12'),
            ('YOTTA_BUILD_DAY',    now.day,         'UTC day 1-31'),
            ('YOTTA_BUILD_HOUR',   now.hour,        'UTC hour 0-24'),
            ('YOTTA_BUILD_MINUTE', now.minute,      'UTC minute 0-59'),
            ('YOTTA_BUILD_SECOND', now.second,      'UTC second 0-61'),
            ('YOTTA_BUILD_UUID',   self.build_uuid, 'unique random UUID for each build'),
        ]
        if vcs_instance is not None:
            commit_id = None
            repotype = vcs_instance.__class__.__name__
            try:
                commit_id = vcs_instance.getCommitId()
            except vcs.VCSNotInstalled as e:
                logger.warning('%s is not installed, VCS status build info is not available', repotype)
                commit_id = None
            except vcs.VCSError as e:
                logger.debug('%s', e)
                logger.warning(
                    'error detecting build info: "%s", build info is not available to the build. Please check that this is a valid %s repository!',
                    str(e).split('\n')[0],
                    repotype
                )
            if commit_id is not None:
                clean_state = int(vcs_instance.isClean())
                description = vcs_instance.getDescription()
                definitions += [
                    ('YOTTA_BUILD_VCS_ID',    commit_id,   'git or mercurial hash'),
                    ('YOTTA_BUILD_VCS_CLEAN', clean_state, 'evaluates true if the version control system was clean, otherwise false'),
                    ('YOTTA_BUILD_VCS_DESCRIPTION', description, 'git describe or mercurial equivalent')
                ]

        for d in definitions:
            preproc_defs += '#define %s %s // %s\n' % d
            cmake_defs   += 'set(%s "%s") # %s\n' % d

        buildinfo_include_file = os.path.join(builddir, 'yotta_build_info.h')
        self._writeFile(
            buildinfo_include_file,
            '#ifndef __YOTTA_BUILD_INFO_H__\n'+
            '#define __YOTTA_BUILD_INFO_H__\n'+
            preproc_defs+
            '#endif // ndef __YOTTA_BUILD_INFO_H__\n'
        )
        return (buildinfo_include_file, cmake_defs)