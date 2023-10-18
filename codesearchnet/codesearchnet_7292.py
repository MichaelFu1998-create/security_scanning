def ensure_local_repo(self):
        """Given a Dusty repo object, clone the remote into Dusty's local repos
        directory if it does not already exist."""
        if os.path.exists(self.managed_path):
            logging.debug('Repo {} already exists'.format(self.remote_path))
            return

        logging.info('Initiating clone of local repo {}'.format(self.remote_path))

        repo_path_parent = parent_dir(self.managed_path)
        if not os.path.exists(repo_path_parent):
            os.makedirs(repo_path_parent)
        with git_error_handling():
            git.Repo.clone_from(self.assemble_remote_path(), self.managed_path)