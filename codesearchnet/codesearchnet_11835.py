def load(self, dump_fn='', prep_only=0, force_upload=0, from_local=0, name=None, site=None, dest_dir=None):
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

        missing_local_dump_error = r.format('Database dump file {dump_fn} does not exist.')

        # Copy snapshot file to target.
        if self.is_local:
            r.env.remote_dump_fn = dump_fn
        else:
            r.env.remote_dump_fn = '/tmp/' + os.path.split(r.env.dump_fn)[-1]

        if not prep_only and not self.is_local:
            if not self.dryrun:
                assert os.path.isfile(r.env.dump_fn), missing_local_dump_error
            r.pc('Uploading MongoDB database snapshot...')
#                 r.put(
#                     local_path=r.env.dump_fn,
#                     remote_path=r.env.remote_dump_fn)
            r.local('rsync -rvz --progress --no-p --no-g '
                '--rsh "ssh -o StrictHostKeyChecking=no -i {key_filename}" '
                '{dump_fn} {user}@{host_string}:{remote_dump_fn}')

        if self.is_local and not prep_only and not self.dryrun:
            assert os.path.isfile(r.env.dump_fn), missing_local_dump_error

        r.run_or_local(r.env.load_command)