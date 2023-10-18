def sort_tags_by_date(self, tags):
        """
        Sort all tags by date.

        :param list(dict) tags: All tags.
        :rtype: list(dict)
        :return: Sorted list of tags.
        """

        if self.options.verbose:
            print("Sorting tags...")
        tags.sort(key=lambda x: self.get_time_of_tag(x))
        tags.reverse()
        return tags