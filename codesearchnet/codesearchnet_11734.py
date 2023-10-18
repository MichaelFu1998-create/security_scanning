def passwordless(self, username, pubkey):
        """
        Configures the user to use an SSL key without a password.
        Assumes you've run generate_keys() first.
        """

        r = self.local_renderer

        r.env.username = username
        r.env.pubkey = pubkey
        if not self.dryrun:
            assert os.path.isfile(r.env.pubkey), \
                'Public key file "%s" does not exist.' % (str(r.env.pubkey),)

        first = os.path.splitext(r.env.pubkey)[0]
        r.env.pubkey = first+'.pub'
        r.env.pemkey = first+'.pem'
        r.env.home = r.env.home_template.format(username=username)

        # Upload the SSH key.
        r.sudo('mkdir -p {home}/.ssh')
        r.sudo('chown -R {user}:{user} {home}/.ssh')

        if r.env.passwordless_method == UPLOAD_KEY:
            put_remote_paths = self.put(local_path=r.env.pubkey)
            r.env.put_remote_path = put_remote_paths[0]
            r.sudo('cat {put_remote_path} >> {home}/.ssh/authorized_keys')
            r.sudo('rm -f {put_remote_path}')
        elif r.env.passwordless_method == CAT_KEY:
            r.env.password = r.env.default_passwords.get(r.env.username, r.genv.password)
            if r.env.password:
                r.local("cat {pubkey} | sshpass -p '{password}' ssh {user}@{host_string} 'cat >> {home}/.ssh/authorized_keys'")
            else:
                r.local("cat {pubkey} | ssh {user}@{host_string} 'cat >> {home}/.ssh/authorized_keys'")
        else:
            raise NotImplementedError

        # Disable password.
        r.sudo('cp /etc/sudoers {tmp_sudoers_fn}')
        r.sudo('echo "{username} ALL=(ALL) NOPASSWD: ALL" >> {tmp_sudoers_fn}')
        r.sudo('sudo EDITOR="cp {tmp_sudoers_fn}" visudo')

        r.sudo('service ssh reload')

        print('You should now be able to login with:')
        r.env.host_string = self.genv.host_string or (self.genv.hosts and self.genv.hosts[0])#self.genv.hostname_hostname
        r.comment('\tssh -i {pemkey} {username}@{host_string}')