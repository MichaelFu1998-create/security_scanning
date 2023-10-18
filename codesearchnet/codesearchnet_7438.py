def upload(self):
        """
        File upload functionality

        Goes through upload steps 0 - 3 (private class methods), and returns
        a dict noting success, failure, or unchanged
        (returning the payload entries with that property as a list for each status)
        """
        result = {"success": [], "failure": [], "unchanged": []}
        self._create_prelim()
        for item in self.payload:
            if "key" not in item:
                result["failure"].append(item)
                continue
            attach = str(self.basedir.joinpath(item["filename"]))
            authdata = self._get_auth(attach, item["key"], md5=item.get("md5", None))
            # no need to keep going if the file exists
            if authdata.get("exists"):
                result["unchanged"].append(item)
                continue
            self._upload_file(authdata, attach, item["key"])
            result["success"].append(item)
        return result