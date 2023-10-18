def experiment_data(self, commit=None, must_contain_results=False):
        """
        :param commit: the commit that all the experiments should have happened or None to include all
        :type commit: str
        :param must_contain_results: include only tags that contain results
        :type must_contain_results: bool
        :return: all the experiment data
        :rtype: dict
        """
        results = {}
        for tag in self.__repository.tags:
            if not tag.name.startswith(self.__tag_prefix):
                continue
            data = json.loads(tag.tag.message)
            if "results" not in data and must_contain_results:
                continue
            if commit is not None and tag.tag.object.hexsha != name_to_object(self.__repository, commit).hexsha:
                continue
            results[tag.name] = data
        return results