def migrate(self, app='', migration='', site=None, fake=0, ignore_errors=None, skip_databases=None, database=None, migrate_apps='', delete_ghosts=1):
        """
        Runs the standard South migrate command for one or more sites.
        """
    #     Note, to pass a comma-delimted list in a fab command, escape the comma with a back slash.
    #
    #         e.g.
    #
    #             fab staging dj.migrate:migrate_apps=oneapp\,twoapp\,threeapp

        r = self.local_renderer

        ignore_errors = int(r.env.ignore_migration_errors if ignore_errors is None else ignore_errors)

        delete_ghosts = int(delete_ghosts)

        post_south = self.version_tuple >= (1, 7, 0)

        if self.version_tuple >= (1, 9, 0):
            delete_ghosts = 0

        skip_databases = (skip_databases or '')
        if isinstance(skip_databases, six.string_types):
            skip_databases = [_.strip() for _ in skip_databases.split(',') if _.strip()]

        migrate_apps = migrate_apps or ''
        migrate_apps = [
            _.strip().split('.')[-1]
            for _ in migrate_apps.strip().split(',')
            if _.strip()
        ]
        if app:
            migrate_apps.append(app)

        r.env.migrate_migration = migration or ''
        r.env.migrate_fake_str = '--fake' if int(fake) else ''
        r.env.migrate_database = '--database=%s' % database if database else ''
        r.env.migrate_merge = '--merge' if not post_south else ''
        r.env.delete_ghosts = '--delete-ghost-migrations' if delete_ghosts and not post_south else ''
        self.vprint('project_dir0:', r.env.project_dir, r.genv.get('dj_project_dir'), r.genv.get('project_dir'))
        self.vprint('migrate_apps:', migrate_apps)

        if self.is_local:
            r.env.project_dir = r.env.local_project_dir

        # CS 2017-3-29 Don't bypass the iterator. That causes reversion to the global env that could corrupt the generated commands.
        #databases = list(self.iter_unique_databases(site=site))#TODO:remove
        # CS 2017-4-24 Don't specify a single site as the default when none is supplied. Otherwise all other sites will be ignored.
        #site = site or self.genv.SITE
        site = site or ALL
        databases = self.iter_unique_databases(site=site)
        for _site, site_data in databases:
            self.vprint('-'*80, file=sys.stderr)
            self.vprint('site:', _site, file=sys.stderr)

            if self.env.available_sites_by_host:
                hostname = self.current_hostname
                sites_on_host = self.env.available_sites_by_host.get(hostname, [])
                if sites_on_host and _site not in sites_on_host:
                    self.vprint('skipping site:', _site, sites_on_host, file=sys.stderr)
                    continue

            if not migrate_apps:
                migrate_apps.append(' ')

            for _app in migrate_apps:
                # In cases where we're migrating built-in apps or apps with dotted names
                # e.g. django.contrib.auth, extract the name used for the migrate command.
                r.env.migrate_app = _app.split('.')[-1]
                self.vprint('project_dir1:', r.env.project_dir, r.genv.get('dj_project_dir'), r.genv.get('project_dir'))
                r.env.SITE = _site
                with self.settings(warn_only=ignore_errors):
                    r.run_or_local(
                        'export SITE={SITE}; export ROLE={ROLE}; {migrate_pre_command} cd {project_dir}; '
                        '{manage_cmd} migrate --noinput {migrate_merge} --traceback '
                        '{migrate_database} {delete_ghosts} {migrate_app} {migrate_migration} '
                        '{migrate_fake_str}')