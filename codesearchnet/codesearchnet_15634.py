def filter_between_tags(self, all_tags):
        """
        Filter tags according between_tags option.

        :param list(dict) all_tags: Pre-filtered tags.
        :rtype: list(dict)
        :return: Filtered tags.
        """

        tag_names = [t["name"] for t in all_tags]
        between_tags = []
        for tag in self.options.between_tags:
            try:
                idx = tag_names.index(tag)
            except ValueError:
                raise ChangelogGeneratorError(
                    "ERROR: can't find tag {0}, specified with "
                    "--between-tags option.".format(tag))
            between_tags.append(all_tags[idx])

        between_tags = self.sort_tags_by_date(between_tags)

        if len(between_tags) == 1:
            # if option --between-tags was only 1 tag given, duplicate it
            # to generate the changelog only for that one tag.
            between_tags.append(between_tags[0])

        older = self.get_time_of_tag(between_tags[1])
        newer = self.get_time_of_tag(between_tags[0])

        for tag in all_tags:
            if older < self.get_time_of_tag(tag) < newer:
                between_tags.append(tag)
        if older == newer:
            between_tags.pop(0)
        return between_tags