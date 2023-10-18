def syncdb(self, site=None, all=0, database=None, ignore_errors=1): # pylint: disable=redefined-builtin
        """
        Runs the standard Django syncdb command for one or more sites.
        """
        r = self.local_renderer

        ignore_errors = int(ignore_errors)

        post_south = self.version_tuple >= (1, 7, 0)

        use_run_syncdb = self.version_tuple >= (1, 9, 0)

        # DEPRECATED: removed in Django>=1.7
        r.env.db_syncdb_all_flag = '--all' if int(all) else ''

        r.env.db_syncdb_database = ''
        if database:
            r.env.db_syncdb_database = ' --database=%s' % database

        if self.is_local:
            r.env.project_dir = r.env.local_project_dir

        site = site or self.genv.SITE
        for _site, site_data in r.iter_unique_databases(site=site):
            r.env.SITE = _site
            with self.settings(warn_only=ignore_errors):
                if post_south:
                    if use_run_syncdb:
                        r.run_or_local(
                            'export SITE={SITE}; export ROLE={ROLE}; cd {project_dir}; '
                            '{manage_cmd} migrate --run-syncdb --noinput {db_syncdb_database}')
                    else:
                        # Between Django>=1.7,<1.9 we can only do a regular migrate, no true syncdb.
                        r.run_or_local(
                            'export SITE={SITE}; export ROLE={ROLE}; cd {project_dir}; '
                            '{manage_cmd} migrate --noinput {db_syncdb_database}')
                else:
                    r.run_or_local(
                        'export SITE={SITE}; export ROLE={ROLE}; cd {project_dir}; '
                        '{manage_cmd} syncdb --noinput {db_syncdb_all_flag} {db_syncdb_database}')