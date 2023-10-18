def generate_keys(self, username, hostname):
        """
        Generates *.pem and *.pub key files suitable for setting up passwordless SSH.
        """

        r = self.local_renderer

        #r.env.key_filename = r.env.key_filename or env.key_filename
        #assert r.env.key_filename, 'r.env.key_filename or env.key_filename must be set. e.g. roles/role/app_name-role.pem'
        r.env.key_filename = self.env.key_filename_template.format(
            ROLE=self.genv.ROLE,
            host=hostname,
            username=username,
        )
        if os.path.isfile(r.env.key_filename):
            r.pc('Key file {key_filename} already exists. Skipping generation.'.format(**r.env))
        else:
            r.local("ssh-keygen -t {key_type} -b {key_bits} -f {key_filename} -N ''")
            r.local('chmod {key_perms} {key_filename}')
            if r.env.key_filename.endswith('.pem'):
                src = r.env.key_filename+'.pub'
                dst = (r.env.key_filename+'.pub').replace('.pem', '')
#                 print('generate_keys:', src, dst)
                r.env.src = src
                r.env.dst = dst
                r.local('mv {src} {dst}')
        return r.env.key_filename