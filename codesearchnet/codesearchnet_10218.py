def __prune_search_template(self, extract_as_keys, search_template):
        """
        Returns a new search template, but the new template has only the extract_as_keys given.

        :param extract_as_keys: List of extract as keys to keep
        :param search_template: The search template to prune
        :return: New search template with pruned columns
        """

        data = {
            "extract_as_keys":
                extract_as_keys,
            "search_template":
                search_template
        }

        failure_message = "Failed to prune a search template"

        return self._get_success_json(self._post_json(
            'v1/search_templates/prune-to-extract-as', data, failure_message=failure_message))['data']