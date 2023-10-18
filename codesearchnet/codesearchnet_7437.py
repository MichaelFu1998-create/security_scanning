def _register_upload(self, authdata, reg_key):
        """
        Step 3: upload successful, so register it
        """
        reg_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "If-None-Match": "*",
        }
        reg_headers.update(self.zinstance.default_headers())
        reg_data = {"upload": authdata.get("uploadKey")}
        upload_reg = requests.post(
            url=self.zinstance.endpoint
            + "/{t}/{u}/items/{i}/file".format(
                t=self.zinstance.library_type, u=self.zinstance.library_id, i=reg_key
            ),
            data=reg_data,
            headers=dict(reg_headers),
        )
        try:
            upload_reg.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(upload_reg)