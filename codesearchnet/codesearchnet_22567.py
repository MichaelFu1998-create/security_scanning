def __tag_repo(self, data, repository):
        """
        Tag the current repository.
        :param data: a dictionary containing the data about the experiment
        :type data: dict
        """
        assert self.__tag_name not in [t.name for t in repository.tags]
        return TagReference.create(repository, self.__tag_name, message=json.dumps(data))