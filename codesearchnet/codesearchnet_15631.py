def get_filtered_tags(self, all_tags):
        """
        Return tags after filtering tags in lists provided by
        option: --between-tags & --exclude-tags

        :param list(dict) all_tags: All tags.
        :rtype: list(dict)
        :return: Filtered tags.
        """

        filtered_tags = self.filter_since_tag(all_tags)
        if self.options.between_tags:
            filtered_tags = self.filter_between_tags(filtered_tags)
        if self.options.due_tag:
            filtered_tags = self.filter_due_tag(filtered_tags)
        return self.filter_excluded_tags(filtered_tags)