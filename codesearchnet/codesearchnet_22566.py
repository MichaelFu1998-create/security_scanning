def record_results(self, results):
        """
        Record the results of this experiment, by updating the tag.
        :param results: A dictionary containing the results of the experiment.
        :type results: dict
        """
        repository = Repo(self.__repository_directory, search_parent_directories=True)
        for tag in repository.tags:
            if tag.name == self.__tag_name:
                tag_object = tag
                break
        else:
            raise Exception("Experiment tag has been deleted since experiment started")
        data = json.loads(tag_object.tag.message)
        data["results"] = results
        TagReference.create(repository, self.__tag_name, message=json.dumps(data),
                            ref=tag_object.tag.object, force=True)
        self.__results_recorded = True