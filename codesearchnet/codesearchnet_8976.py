def _auto_client_files(cls, client, ca_path=None, ca_contents=None, cert_path=None,
                           cert_contents=None, key_path=None, key_contents=None):
        """
        returns a list of NetJSON extra files for automatically generated clients
        produces side effects in ``client`` dictionary
        """
        files = []
        if ca_path and ca_contents:
            client['ca'] = ca_path
            files.append(dict(path=ca_path,
                              contents=ca_contents,
                              mode=DEFAULT_FILE_MODE))
        if cert_path and cert_contents:
            client['cert'] = cert_path
            files.append(dict(path=cert_path,
                              contents=cert_contents,
                              mode=DEFAULT_FILE_MODE))
        if key_path and key_contents:
            client['key'] = key_path
            files.append(dict(path=key_path,
                              contents=key_contents,
                              mode=DEFAULT_FILE_MODE,))
        return files