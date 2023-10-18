def attachment_both(self, files, parentid=None):
        """
        Add child attachments using title, filename
        Arguments:
        One or more lists or tuples containing title, file path
        An optional Item ID, which will create child attachments
        """
        orig = self._attachment_template("imported_file")
        to_add = [orig.copy() for f in files]
        for idx, tmplt in enumerate(to_add):
            tmplt["title"] = files[idx][0]
            tmplt["filename"] = files[idx][1]
        if parentid:
            return self._attachment(to_add, parentid)
        else:
            return self._attachment(to_add)