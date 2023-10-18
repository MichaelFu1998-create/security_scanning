def dump(self, dest_dir=None, to_local=1, from_local=0, archive=0, dump_fn=None, name=None, site=None, use_sudo=0, cleanup=1):
        """
        Exports the target database to a single transportable file on the localhost,
        appropriate for loading using load().
        """
        r = self.local_renderer

        site = site or self.genv.SITE

        r = self.database_renderer(name=name, site=site)

        # Load optional site-specific command, if given.
        try:
            r.env.dump_command = self.genv.sites[site]['postgresql_dump_command']
        except KeyError:
            pass

        use_sudo = int(use_sudo)

        from_local = int(from_local)

        to_local = int(to_local)

        dump_fn = dump_fn or r.env.dump_fn_template

        # Render the snapshot filename.
        r.env.dump_fn = self.get_default_db_fn(
            fn_template=dump_fn,
            dest_dir=dest_dir,
            name=name,
            site=site,
        )

        # Dump the database to a snapshot file.
        #if not os.path.isfile(os.path.abspath(r.env.dump_fn))):
        r.pc('Dumping database snapshot.')
        if from_local:
            r.local(r.env.dump_command)
        elif use_sudo:
            r.sudo(r.env.dump_command)
        else:
            r.run(r.env.dump_command)

        # Download the database dump file on the remote host to localhost.
        if not from_local and to_local:
            r.pc('Downloading database snapshot to localhost.')
            r.local('rsync -rvz --progress --recursive --no-p --no-g '
                '--rsh "ssh -o StrictHostKeyChecking=no -i {key_filename}" {user}@{host_string}:{dump_fn} {dump_fn}')

            # Delete the snapshot file on the remote system.
            if int(cleanup):
                r.pc('Deleting database snapshot on remote host.')
                r.sudo('rm {dump_fn}')

        # Move the database snapshot to an archive directory.
        if to_local and int(archive):
            r.pc('Archiving database snapshot.')
            db_fn = r.render_fn(r.env.dump_fn)
            r.env.archive_fn = '%s/%s' % (env.db_dump_archive_dir, os.path.split(db_fn)[-1])
            r.local('mv %s %s' % (db_fn, env.archive_fn))

        return r.env.dump_fn