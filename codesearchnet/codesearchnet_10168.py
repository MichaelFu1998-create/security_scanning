def to_dict(self):
        """
        Converts the column to a dictionary representation accepted
        by the Citrination server.

        :return: Dictionary with basic options, plus any column type specific
            options held under the "options" key
        :rtype: dict
        """
        return {
            "type": self.type,
            "name": self.name,
            "group_by_key": self.group_by_key,
            "role": self.role,
            "units": self.units,
            "options": self.build_options()
        }