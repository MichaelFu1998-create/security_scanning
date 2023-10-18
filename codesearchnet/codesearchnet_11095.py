def _get_resource(self, label: str, source: dict, resource_type: str):
        """
        Generic resoure fetcher handling errors.

        Args:
            label (str): The label to fetch
            source (dict): The dictionary to look up the label
            resource_type str: The display name of the resource type (used in errors)
        """
        try:
            return source[label]
        except KeyError:
            raise ValueError("Cannot find {0} with label '{1}'.\nExisting {0} labels: {2}".format(
                resource_type, label, list(source.keys())))