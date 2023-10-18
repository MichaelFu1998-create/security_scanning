def init(self):
        """
        Creates the virtual environment.
        """
        r = self.local_renderer

#         if self.virtualenv_exists():
#             print('virtualenv exists')
#             return

        print('Creating new virtual environment...')
        with self.settings(warn_only=True):
            cmd = '[ ! -d {virtualenv_dir} ] && virtualenv --no-site-packages {virtualenv_dir} || true'
            if self.is_local:
                r.run_or_local(cmd)
            else:
                r.sudo(cmd)