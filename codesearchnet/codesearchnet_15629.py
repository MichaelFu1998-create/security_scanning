def version_of_first_item(self):
        """
        Try to detect the newest tag from self.options.base, otherwise
        return a special value indicating the creation of the repo.

        :rtype: str
        :return: Tag name to use as 'oldest' tag. May be special value,
                 indicating the creation of the repo.
        """
        try:
            sections = read_changelog(self.options)
            return sections[0]["version"]
        except(IOError, TypeError):
            return self.get_temp_tag_for_repo_creation()