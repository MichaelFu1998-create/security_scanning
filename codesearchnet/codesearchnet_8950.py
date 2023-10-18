def get_copy(dict_, key, default=None):
        """
        Looks for a key in a dictionary, if found returns
        a deepcopied value, otherwise returns default value
        """
        value = dict_.get(key, default)
        if value:
            return deepcopy(value)
        return value