def _get_auth(self, attachment, reg_key, md5=None):
        """
        Step 1: get upload authorisation for a file
        """
        mtypes = mimetypes.guess_type(attachment)
        digest = hashlib.md5()
        with open(attachment, "rb") as att:
            for chunk in iter(lambda: att.read(8192), b""):
                digest.update(chunk)
        auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if not md5:
            auth_headers["If-None-Match"] = "*"
        else:
            # docs specify that for existing file we use this
            auth_headers["If-Match"] = md5
        auth_headers.update(self.zinstance.default_headers())
        data = {
            "md5": digest.hexdigest(),
            "filename": os.path.basename(attachment),
            "filesize": os.path.getsize(attachment),
            "mtime": str(int(os.path.getmtime(attachment) * 1000)),
            "contentType": mtypes[0] or "application/octet-stream",
            "charset": mtypes[1],
            "params": 1,
        }
        auth_req = requests.post(
            url=self.zinstance.endpoint
            + "/{t}/{u}/items/{i}/file".format(
                t=self.zinstance.library_type, u=self.zinstance.library_id, i=reg_key
            ),
            data=data,
            headers=auth_headers,
        )
        try:
            auth_req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(auth_req)
        return auth_req.json()