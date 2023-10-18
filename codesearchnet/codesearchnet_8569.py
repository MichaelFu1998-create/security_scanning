def get_program_type_by_slug(self, slug):
        """
        Get a program type by its slug.

        Arguments:
            slug (str): The slug to identify the program type.

        Returns:
            dict: A program type object.

        """
        return self._load_data(
            self.PROGRAM_TYPES_ENDPOINT,
            resource_id=slug,
            default=None,
        )