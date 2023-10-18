def upload_template(self, filename, destination, context=None, use_jinja=False,
                        template_dir=None, use_sudo=False, backup=True,
                        mirror_local_mode=False, mode=None,
                        mkdir=False, chown=False, user=None):
        """
        Upload a template file.

        This is a wrapper around :func:`fabric.contrib.files.upload_template`
        that adds some extra parameters.

        If ``mkdir`` is True, then the remote directory will be created, as
        the current user or as ``user`` if specified.

        If ``chown`` is True, then it will ensure that the current user (or
        ``user`` if specified) is the owner of the remote file.
        """

        if mkdir:
            remote_dir = os.path.dirname(destination)
            if use_sudo:
                self.sudo('mkdir -p %s' % quote(remote_dir), user=user)
            else:
                self.run('mkdir -p %s' % quote(remote_dir))

        if not self.dryrun:
            _upload_template(
                filename=filename,
                destination=destination,
                context=context,
                use_jinja=use_jinja,
                template_dir=template_dir,
                use_sudo=use_sudo,
                backup=backup,
                mirror_local_mode=mirror_local_mode,
                mode=mode,
            )

        if chown:
            if user is None:
                user = self.genv.user
            run_as_root('chown %s: %s' % (user, quote(destination)))