def _sort_by(key):
    """
    High order function for sort methods.
    """

    @staticmethod
    def sort_by(p_list, reverse=False):
        return sorted(
            p_list,
            key=lambda p: getattr(p, key),
            reverse=reverse,
        )

    return sort_by