def delete(self, experiment_name):
        """
        Delete an experiment by removing the associated tag.
        :param experiment_name: the name of the experiment to be deleted
        :type experiment_name: str
        :rtype bool
        :return if deleting succeeded
        """
        if not experiment_name.startswith(self.__tag_prefix):
            target_tag = self.__tag_prefix + experiment_name
        else:
            target_tag = experiment_name
        if target_tag not in [t.name for t in self.__repository.tags]:
            return False
        self.__repository.delete_tag(target_tag)
        return target_tag not in [t.name for t in self.__repository.tags]