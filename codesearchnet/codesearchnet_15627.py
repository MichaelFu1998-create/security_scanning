def get_time_of_tag(self, tag):
        """
        Get date and time for tag, fetching it if not already cached.

        :param dict tag: Tag to get the datetime for.
        :rtype: datetime
        :return: datetime for specified tag.
        """

        if not tag:
            raise ChangelogGeneratorError("tag is nil")

        name_of_tag = tag["name"]
        time_for_name = self.tag_times_dict.get(name_of_tag, None)
        if time_for_name:
            return time_for_name
        else:
            time_string = self.fetcher.fetch_date_of_tag(tag)
            try:
                self.tag_times_dict[name_of_tag] = \
                    timestring_to_datetime(time_string)
            except UnicodeWarning:
                print("ERROR ERROR:", tag)
                self.tag_times_dict[name_of_tag] = \
                    timestring_to_datetime(time_string)
            return self.tag_times_dict[name_of_tag]