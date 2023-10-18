def filter_since_tag(self, all_tags):
        """
        Filter tags according since_tag option.

        :param list(dict) all_tags: All tags.
        :rtype: list(dict)
        :return: Filtered tags.
        """

        tag = self.detect_since_tag()
        if not tag or tag == REPO_CREATED_TAG_NAME:
            return copy.deepcopy(all_tags)

        filtered_tags = []
        tag_names = [t["name"] for t in all_tags]
        try:
            idx = tag_names.index(tag)
        except ValueError:
            self.warn_if_tag_not_found(tag, "since-tag")
            return copy.deepcopy(all_tags)

        since_tag = all_tags[idx]
        since_date = self.get_time_of_tag(since_tag)
        for t in all_tags:
            tag_date = self.get_time_of_tag(t)
            if since_date <= tag_date:
                filtered_tags.append(t)
        return filtered_tags