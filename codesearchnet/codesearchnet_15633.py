def filter_due_tag(self, all_tags):
        """
        Filter tags according due_tag option.

        :param list(dict) all_tags: Pre-filtered tags.
        :rtype: list(dict)
        :return: Filtered tags.
        """

        filtered_tags = []
        tag = self.options.due_tag
        tag_names = [t["name"] for t in all_tags]
        try:
            idx = tag_names.index(tag)
        except ValueError:
            self.warn_if_tag_not_found(tag, "due-tag")
            return copy.deepcopy(all_tags)

        due_tag = all_tags[idx]
        due_date = self.get_time_of_tag(due_tag)
        for t in all_tags:
            tag_date = self.get_time_of_tag(t)
            if tag_date <= due_date:
                filtered_tags.append(t)
        return filtered_tags