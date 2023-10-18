def __get_files_to_be_added(self, repository):
        """
        :return: the files that have been modified and can be added
        """
        for root, dirs, files in os.walk(repository.working_dir):
            for f in files:
                relative_path = os.path.join(root, f)[len(repository.working_dir) + 1:]
                try:
                    repository.head.commit.tree[relative_path] # will fail if not tracked
                    yield relative_path
                except:
                    pass