def _upload_file(self, authdata, attachment, reg_key):
        """
        Step 2: auth successful, and file not on server
        zotero.org/support/dev/server_api/file_upload#a_full_upload

        reg_key isn't used, but we need to pass it through to Step 3
        """
        upload_dict = authdata[
            "params"
        ]  # using params now since prefix/suffix concat was giving ConnectionError
        # must pass tuple of tuples not dict to ensure key comes first
        upload_list = [("key", upload_dict["key"])]
        for k in upload_dict:
            if k != "key":
                upload_list.append((k, upload_dict[k]))
        # The prior code for attaching file gave me content not match md5
        # errors
        upload_list.append(("file", open(attachment, "rb").read()))
        upload_pairs = tuple(upload_list)
        try:
            upload = requests.post(
                url=authdata["url"],
                files=upload_pairs,
                headers={
                    # "Content-Type": authdata['contentType'],
                    "User-Agent": "Pyzotero/%s"
                    % __version__
                },
            )
        except (requests.exceptions.ConnectionError):
            raise ze.UploadError("ConnectionError")
        try:
            upload.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(upload)
        # now check the responses
        return self._register_upload(authdata, reg_key)