def apply_exclude_tags_regex(self, all_tags):
        """
        Filter tags according exclude_tags_regex option.

        :param list(dict) all_tags: Pre-filtered tags.
        :rtype: list(dict)
        :return: Filtered tags.
        """
        filtered = []
        for tag in all_tags:
            if not re.match(self.options.exclude_tags_regex, tag["name"]):
                filtered.append(tag)
        if len(all_tags) == len(filtered):
            self.warn_if_nonmatching_regex()
        return filtered