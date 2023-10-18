def perform_upload(self, upload_token, filename, **kwargs):
        """
        Upload a file into a given item (or just to the public folder if the
        item is not specified.

        :param upload_token: The upload token (returned by
            generate_upload_token)
        :type upload_token: string
        :param filename: The upload filename. Also used as the path to the
            file, if 'filepath' is not set.
        :type filename: string
        :param mode: (optional) Stream or multipart. Default is stream.
        :type mode: string
        :param folder_id: (optional) The id of the folder to upload into.
        :type folder_id: int | long
        :param item_id: (optional) If set, will append item ``bitstreams`` to
            the latest revision (or the one set using :param:`revision` ) of
            the existing item.
        :type item_id: int | long
        :param revision: (optional) If set, will add a new file into an
            existing revision. Set this to 'head' to add to the most recent
            revision.
        :type revision: string | int | long
        :param filepath: (optional) The path to the file.
        :type filepath: string
        :param create_additional_revision: (optional) If set, will create a
            new revision in the existing item.
        :type create_additional_revision: bool
        :returns: Dictionary containing the details of the item created or
            changed.
        :rtype: dict
        """
        parameters = dict()
        parameters['uploadtoken'] = upload_token
        parameters['filename'] = filename

        try:
            create_additional_revision = kwargs['create_additional_revision']
        except KeyError:
            create_additional_revision = False

        if not create_additional_revision:
            parameters['revision'] = 'head'
        optional_keys = ['mode', 'folderid', 'item_id', 'itemid', 'revision']
        for key in optional_keys:
            if key in kwargs:
                if key == 'item_id':
                    parameters['itemid'] = kwargs[key]
                    continue
                if key == 'folder_id':
                    parameters['folderid'] = kwargs[key]
                    continue
                parameters[key] = kwargs[key]

        # We may want a different name than path
        file_payload = open(kwargs.get('filepath', filename), 'rb')
        # Arcane getting of the file size using fstat. More details can be
        # found in the python library docs
        parameters['length'] = os.fstat(file_payload.fileno()).st_size

        response = self.request('midas.upload.perform', parameters,
                                file_payload)
        return response