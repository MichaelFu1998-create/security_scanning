def _create_prelim(self):
        """
        Step 0: Register intent to upload files
        """
        self._verify(self.payload)
        if "key" in self.payload[0] and self.payload[0]["key"]:
            if next((i for i in self.payload if "key" not in i), False):
                raise ze.UnsupportedParams(
                    "Can't pass payload entries with and without keys to Zupload"
                )
            return None  # Don't do anything if payload comes with keys
        liblevel = "/{t}/{u}/items"
        # Create one or more new attachments
        headers = {"Zotero-Write-Token": token(), "Content-Type": "application/json"}
        headers.update(self.zinstance.default_headers())
        # If we have a Parent ID, add it as a parentItem
        if self.parentid:
            for child in self.payload:
                child["parentItem"] = self.parentid
        to_send = json.dumps(self.payload)
        req = requests.post(
            url=self.zinstance.endpoint
            + liblevel.format(
                t=self.zinstance.library_type, u=self.zinstance.library_id
            ),
            data=to_send,
            headers=headers,
        )
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        data = req.json()
        for k in data["success"]:
            self.payload[int(k)]["key"] = data["success"][k]
        return data