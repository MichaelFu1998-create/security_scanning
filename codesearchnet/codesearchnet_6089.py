def get_display_info(self):
        """Return additional info dictionary for displaying (optional).

        This information is not part of the DAV specification, but meant for use
        by the dir browser middleware.

        This default implementation returns ``{'type': '...'}``
        """
        if self.is_collection:
            return {"type": "Directory"}
        elif os.extsep in self.name:
            ext = self.name.split(os.extsep)[-1].upper()
            if len(ext) < 5:
                return {"type": "{}-File".format(ext)}
        return {"type": "File"}