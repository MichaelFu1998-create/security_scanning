def user_and_project_from_git(self, options, arg0=None, arg1=None):
        """ Detects user and project from git. """
        user, project = self.user_project_from_option(options, arg0, arg1)
        if user and project:
            return user, project

        try:
            remote = subprocess.check_output(
                [
                    'git', 'config', '--get',
                    'remote.{0}.url'.format(options.git_remote)
                ]
            )
        except subprocess.CalledProcessError:
            return None, None
        except WindowsError:
            print("git binary not found.")
            exit(1)
        else:
            return self.user_project_from_remote(remote)