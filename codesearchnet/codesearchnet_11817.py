def load(self, dump_fn='', prep_only=0, force_upload=0, from_local=0, name=None, site=None, dest_dir=None, force_host=None):
        """
        Restores a database snapshot onto the target database server.

        If prep_only=1, commands for preparing the load will be generated,
        but not the command to finally load the snapshot.
        """

        r = self.database_renderer(name=name, site=site)

        # Render the snapshot filename.
        r.env.dump_fn = self.get_default_db_fn(fn_template=dump_fn, dest_dir=dest_dir)

        from_local = int(from_local)

        prep_only = int(prep_only)

        missing_local_dump_error = r.format(
            "Database dump file {dump_fn} does not exist."
        )

        # Copy snapshot file to target.
        if self.is_local:
            r.env.remote_dump_fn = dump_fn
        else:
            r.env.remote_dump_fn = '/tmp/' + os.path.split(r.env.dump_fn)[-1]

        if not prep_only and not self.is_local:
            if not self.dryrun:
                assert os.path.isfile(r.env.dump_fn), missing_local_dump_error
            #r.pc('Uploading PostgreSQL database snapshot...')
#                 r.put(
#                     local_path=r.env.dump_fn,
#                     remote_path=r.env.remote_dump_fn)
            #r.local('rsync -rvz --progress --no-p --no-g '
                #'--rsh "ssh -o StrictHostKeyChecking=no -i {key_filename}" '
                #'{dump_fn} {user}@{host_string}:{remote_dump_fn}')
            self.upload_snapshot(name=name, site=site, local_dump_fn=r.env.dump_fn, remote_dump_fn=r.env.remote_dump_fn)

        if self.is_local and not prep_only and not self.dryrun:
            assert os.path.isfile(r.env.dump_fn), missing_local_dump_error

        if force_host:
            r.env.db_host = force_host

        with settings(warn_only=True):
            r.sudo('dropdb --if-exists --no-password --user={db_root_username} --host={db_host} {db_name}', user=r.env.postgres_user)

        r.sudo('psql --no-password --user={db_root_username} --host={db_host} -c "CREATE DATABASE {db_name};"', user=r.env.postgres_user)

        with settings(warn_only=True):

            if r.env.engine == POSTGIS:
                r.sudo('psql --user={db_root_username} --no-password --dbname={db_name} --host={db_host} --command="CREATE EXTENSION postgis;"',
                    user=r.env.postgres_user)
                r.sudo('psql --user={db_root_username} --no-password --dbname={db_name} --host={db_host} --command="CREATE EXTENSION postgis_topology;"',
                    user=r.env.postgres_user)

        with settings(warn_only=True):
            r.sudo('psql --user={db_root_username} --host={db_host} -c "REASSIGN OWNED BY {db_user} TO {db_root_username};"', user=r.env.postgres_user)

        with settings(warn_only=True):
            r.sudo('psql --user={db_root_username} --host={db_host} -c "DROP OWNED BY {db_user} CASCADE;"', user=r.env.postgres_user)

        r.sudo('psql --user={db_root_username} --host={db_host} -c "DROP USER IF EXISTS {db_user}; '
            'CREATE USER {db_user} WITH PASSWORD \'{db_password}\'; '
            'GRANT ALL PRIVILEGES ON DATABASE {db_name} to {db_user};"', user=r.env.postgres_user)
        for createlang in r.env.createlangs:
            r.env.createlang = createlang
            r.sudo('createlang -U {db_root_username} --host={db_host} {createlang} {db_name} || true', user=r.env.postgres_user)

        if not prep_only:
            # Ignore errors needed to work around bug "ERROR:  schema "public" already exists", which is thrown in 9.6 even if we use --clean and --if-exists?
            with settings(warn_only=True):
                r.sudo(r.env.load_command, user=r.env.postgres_user)