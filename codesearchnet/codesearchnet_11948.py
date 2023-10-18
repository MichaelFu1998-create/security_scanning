def load(self, dump_fn='', prep_only=0, force_upload=0, from_local=0, name=None, site=None, dest_dir=None, force_host=None):
        """
        Restores a database snapshot onto the target database server.

        If prep_only=1, commands for preparing the load will be generated,
        but not the command to finally load the snapshot.
        """

        r = self.database_renderer(name=name, site=site)
        r.pc('Loading database snapshot.')

        # Render the snapshot filename.
        r.env.dump_fn = self.get_default_db_fn(fn_template=dump_fn, dest_dir=dest_dir).strip()

        from_local = int(from_local)

        prep_only = int(prep_only)

        missing_local_dump_error = r.format("Database dump file {dump_fn} does not exist.")

        # Copy snapshot file to target.
        if self.is_local:
            r.env.remote_dump_fn = dump_fn
        else:
            r.env.remote_dump_fn = '/tmp/' + os.path.split(r.env.dump_fn)[-1]

        if not prep_only and not self.is_local:
            #if int(force_upload) or (not self.is_local and not r.file_exists(r.env.remote_dump_fn)):
            if not self.dryrun:
                assert os.path.isfile(r.env.dump_fn), missing_local_dump_error
            #if self.verbose:
                #print('Uploading MySQL database snapshot...')
            #r.put(
                #local_path=r.env.dump_fn,
                #remote_path=r.env.remote_dump_fn)
            self.upload_snapshot(name=name, site=site)

        if self.is_local and not prep_only and not self.dryrun:
            assert os.path.isfile(r.env.dump_fn), missing_local_dump_error

        if force_host:
            r.env.db_host = force_host

        # Drop the database if it's there.
        r.run("mysql -v -h {db_host} -u {db_root_username} -p'{db_root_password}' --execute='DROP DATABASE IF EXISTS {db_name}'")

        # Now, create the database.
        r.run("mysqladmin -h {db_host} -u {db_root_username} -p'{db_root_password}' create {db_name}")

        # Create user
        with settings(warn_only=True):
            r.run("mysql -v -h {db_host} -u {db_root_username} -p'{db_root_password}' --execute=\"DROP USER '{db_user}'@'%%';"
                "FLUSH PRIVILEGES;\"")
        with settings(warn_only=True):
            r.run("mysql -v -h {db_host} -u {db_root_username} -p'{db_root_password}' --execute=\"CREATE USER '{db_user}'@'%%' IDENTIFIED BY '{db_password}'; "
                "GRANT ALL PRIVILEGES ON *.* TO '{db_user}'@'%%' WITH GRANT OPTION; "
                "FLUSH PRIVILEGES;\"")
        self.set_collation(name=name, site=site)

        self.set_max_packet_size(name=name, site=site)

        # Run any server-specific commands (e.g. to setup permissions) before
        # we load the data.
        for command in r.env.preload_commands:
            r.run(command)

        # Restore the database content from the dump file.
        if not prep_only:
            r.run(r.env.load_command)

        self.set_collation(name=name, site=site)