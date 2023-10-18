def _sort_course_modes(self, modes):
        """
        Sort the course mode dictionaries by slug according to the COURSE_MODE_SORT_ORDER constant.

        Arguments:
            modes (list): A list of course mode dictionaries.
        Returns:
            list: A list with the course modes dictionaries sorted by slug.

        """
        def slug_weight(mode):
            """
            Assign a weight to the course mode dictionary based on the position of its slug in the sorting list.
            """
            sorting_slugs = COURSE_MODE_SORT_ORDER
            sorting_slugs_size = len(sorting_slugs)
            if mode['slug'] in sorting_slugs:
                return sorting_slugs_size - sorting_slugs.index(mode['slug'])
            return 0
        # Sort slug weights in descending order
        return sorted(modes, key=slug_weight, reverse=True)