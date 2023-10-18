def apply_exclude_tags(self, all_tags):
        """
        Filter tags according exclude_tags option.

        :param list(dict) all_tags: Pre-filtered tags.
        :rtype: list(dict)
        :return: Filtered tags.
        """
        filtered = copy.deepcopy(all_tags)
        for tag in all_tags:
            if tag["name"] not in self.options.exclude_tags:
                self.warn_if_tag_not_found(tag, "exclude-tags")
            else:
                filtered.remove(tag)
        return filtered