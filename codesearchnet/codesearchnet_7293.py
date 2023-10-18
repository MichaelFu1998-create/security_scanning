def update_local_repo(self, force=False):
        """Given a remote path (e.g. github.com/gamechanger/gclib), pull the latest
        commits from master to bring the local copy up to date."""
        self.ensure_local_repo()

        logging.info('Updating local repo {}'.format(self.remote_path))

        managed_repo = git.Repo(self.managed_path)
        with git_error_handling():
            managed_repo.remote().pull('master')
            log_to_client('Updated managed copy of {}'.format(self.remote_path))
        if not self.local_is_up_to_date():
            if force:
                with git_error_handling():
                    managed_repo.git.reset('--hard', 'origin/master')
            else:
                log_to_client('WARNING: couldn\'t update {} because of local conflicts. '
                              'A container may have modified files in the repos\'s directory. '
                              'Your code generally shouldn\'t be manipulating the contents of your repo folder - '
                              'please fix this and run `dusty up`'.format(self.managed_path))