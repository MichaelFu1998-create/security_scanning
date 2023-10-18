def find_working_password(self, usernames=None, host_strings=None):
        """
        Returns the first working combination of username and password for the current host.
        """
        r = self.local_renderer

        if host_strings is None:
            host_strings = []

        if not host_strings:
            host_strings.append(self.genv.host_string)

        if usernames is None:
            usernames = []

        if not usernames:
            usernames.append(self.genv.user)

        for host_string in host_strings:

            for username in usernames:

                passwords = []
                passwords.append(self.genv.user_default_passwords[username])
                passwords.append(self.genv.user_passwords[username])
                passwords.append(self.env.default_password)

                for password in passwords:

                    with settings(warn_only=True):
                        r.env.host_string = host_string
                        r.env.password = password
                        r.env.user = username
                        ret = r._local("sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {user}@{host_string} echo hello", capture=True)
                        #print('ret.return_code:', ret.return_code)
            #             print('ret000:[%s]' % ret)
                        #code 1 = good password, but prompts needed
                        #code 5 = bad password
                        #code 6 = good password, but host public key is unknown

                    if ret.return_code in (1, 6) or 'hello' in ret:
                        # Login succeeded, so we haven't yet changed the password, so use the default password.
                        return host_string, username, password

        raise Exception('No working login found.')