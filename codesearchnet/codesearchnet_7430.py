def delete_tags(self, *payload):
        """
        Delete a group of tags
        pass in up to 50 tags, or use *[tags]

        """
        if len(payload) > 50:
            raise ze.TooManyItems("Only 50 tags or fewer may be deleted")
        modified_tags = " || ".join([tag for tag in payload])
        # first, get version data by getting one tag
        self.tags(limit=1)
        headers = {
            "If-Unmodified-Since-Version": self.request.headers["last-modified-version"]
        }
        headers.update(self.default_headers())
        req = requests.delete(
            url=self.endpoint
            + "/{t}/{u}/tags".format(t=self.library_type, u=self.library_id),
            params={"tag": modified_tags},
            headers=headers,
        )
        self.request = req
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return True