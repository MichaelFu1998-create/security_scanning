def filter_excluded_tags(self, all_tags):
        """
        Filter tags according exclude_tags and exclude_tags_regex option.

        :param list(dict) all_tags: Pre-filtered tags.
        :rtype: list(dict)
        :return: Filtered tags.
        """
        filtered_tags = copy.deepcopy(all_tags)
        if self.options.exclude_tags:
            filtered_tags = self.apply_exclude_tags(filtered_tags)
        if self.options.exclude_tags_regex:
            filtered_tags = self.apply_exclude_tags_regex(filtered_tags)
        return filtered_tags