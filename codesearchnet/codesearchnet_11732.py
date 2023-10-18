def enter_password_change(self, username=None, old_password=None):
        """
        Responds to a forced password change via `passwd` prompts due to password expiration.
        """
        from fabric.state import connections
        from fabric.network import disconnect_all
        r = self.local_renderer
#         print('self.genv.user:', self.genv.user)
#         print('self.env.passwords:', self.env.passwords)
        r.genv.user = r.genv.user or username
        r.pc('Changing password for user {user} via interactive prompts.')
        r.env.old_password = r.env.default_passwords[self.genv.user]
#         print('self.genv.user:', self.genv.user)
#         print('self.env.passwords:', self.env.passwords)
        r.env.new_password = self.env.passwords[self.genv.user]
        if old_password:
            r.env.old_password = old_password
        prompts = {
            '(current) UNIX password: ': r.env.old_password,
            'Enter new UNIX password: ': r.env.new_password,
            'Retype new UNIX password: ': r.env.new_password,
            #"Login password for '%s': " % r.genv.user: r.env.new_password,
#             "Login password for '%s': " % r.genv.user: r.env.old_password,
        }
        print('prompts:', prompts)

        r.env.password = r.env.old_password
        with self.settings(warn_only=True):
            ret = r._local("sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {user}@{host_string} echo hello", capture=True)
            #code 1 = good password, but prompts needed
            #code 5 = bad password
            #code 6 = good password, but host public key is unknown
        if ret.return_code in (1, 6) or 'hello' in ret:
            # Login succeeded, so we haven't yet changed the password, so use the default password.
            self.genv.password = r.env.old_password
        elif self.genv.user in self.genv.user_passwords:
            # Otherwise, use the password or key set in the config.
            self.genv.password = r.env.new_password
        else:
            # Default password fails and there's no current password, so clear.
            self.genv.password = None
        print('using password:', self.genv.password)

        # Note, the correct current password should be set in host.initrole(), not here.
        #r.genv.password = r.env.new_password
        #r.genv.password = r.env.new_password
        with self.settings(prompts=prompts):
            ret = r._run('echo checking for expired password')
            print('ret:[%s]' % ret)
            do_disconnect = 'passwd: password updated successfully' in ret
            print('do_disconnect:', do_disconnect)
            if do_disconnect:
                # We need to disconnect to reset the session or else Linux will again prompt
                # us to change our password.
                disconnect_all()

                # Further logins should require the new password.
                self.genv.password = r.env.new_password