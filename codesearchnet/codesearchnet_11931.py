def initrole(self, check=True):
        """
        Called to set default password login for systems that do not yet have passwordless
        login setup.
        """

        if self.env.original_user is None:
            self.env.original_user = self.genv.user

        if self.env.original_key_filename is None:
            self.env.original_key_filename = self.genv.key_filename

        host_string = None
        user = None
        password = None
        if self.env.login_check:
            host_string, user, password = self.find_working_password(
                usernames=[self.genv.user, self.env.default_user],
                host_strings=[self.genv.host_string, self.env.default_hostname],
            )
            if self.verbose:
                print('host.initrole.host_string:', host_string)
                print('host.initrole.user:', user)
                print('host.initrole.password:', password)

#         needs = True
#         if check:
#             needs = self.needs_initrole(stop_on_error=True)
        needs = False

        if host_string is not None:
            self.genv.host_string = host_string
        if user is not None:
            self.genv.user = user
        if password is not None:
            self.genv.password = password

        if not needs:
            return

        assert self.env.default_hostname, 'No default hostname set.'
        assert self.env.default_user, 'No default user set.'

        self.genv.host_string = self.env.default_hostname
        if self.env.default_hosts:
            self.genv.hosts = self.env.default_hosts
        else:
            self.genv.hosts = [self.env.default_hostname]

        self.genv.user = self.env.default_user
        self.genv.password = self.env.default_password
        self.genv.key_filename = self.env.default_key_filename

        # If the host has been reformatted, the SSH keys will mismatch, throwing an error, so clear them.
        self.purge_keys()

        # Do a test login with the default password to determine which password we should use.
#         r.env.password = self.env.default_password
#         with settings(warn_only=True):
#             ret = r._local("sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {user}@{host_string} echo hello", capture=True)
#             print('ret.return_code:', ret.return_code)
# #             print('ret000:[%s]' % ret)
#             #code 1 = good password, but prompts needed
#             #code 5 = bad password
#             #code 6 = good password, but host public key is unknown
#         if ret.return_code in (1, 6) or 'hello' in ret:
#             # Login succeeded, so we haven't yet changed the password, so use the default password.
#             self.genv.password = self.env.default_password
#         elif self.genv.user in self.genv.user_passwords:
#             # Otherwise, use the password or key set in the config.
#             self.genv.password = self.genv.user_passwords[self.genv.user]
#         else:
#             # Default password fails and there's no current password, so clear.
#             self.genv.password = None
#         self.genv.password = self.find_working_password()
#         print('host.initrole,using password:', self.genv.password)

        # Execute post-init callbacks.
        for task_name in self.env.post_initrole_tasks:
            if self.verbose:
                print('Calling post initrole task %s' % task_name)
            satchel_name, method_name = task_name.split('.')
            satchel = self.get_satchel(name=satchel_name)
            getattr(satchel, method_name)()

        print('^'*80)
        print('host.initrole.host_string:', self.genv.host_string)
        print('host.initrole.user:', self.genv.user)
        print('host.initrole.password:', self.genv.password)