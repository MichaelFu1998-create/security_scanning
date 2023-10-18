def __start_experiment(self, parameters):
        """
        Start an experiment by capturing the state of the code
        :param parameters: a dictionary containing the parameters of the experiment
        :type parameters: dict
        :return: the tag representing this experiment
        :rtype: TagReference
        """
        repository = Repo(self.__repository_directory, search_parent_directories=True)
        if len(repository.untracked_files) > 0:
            logging.warning("Untracked files will not be recorded: %s", repository.untracked_files)
        current_commit = repository.head.commit
        started_state_is_dirty = repository.is_dirty()

        if started_state_is_dirty:
            repository.index.add([p for p in self.__get_files_to_be_added(repository)])
            commit_obj = repository.index.commit("Temporary commit for experiment " + self.__experiment_name)
            sha = commit_obj.hexsha
        else:
            sha = repository.head.object.hexsha

        data = {"parameters": parameters, "started": time.time(), "description": self.__description,
                "commit_sha": sha}
        tag_object = self.__tag_repo(data, repository)

        if started_state_is_dirty:
            repository.head.reset(current_commit, working_tree=False, index=True)

        return tag_object