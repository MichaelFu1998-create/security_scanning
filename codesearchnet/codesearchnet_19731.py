def upload_folder(self, bucket, folder, key=None, skip=None,
                      content_types=None):
        """Recursively upload a ``folder`` into a backet.

        :param bucket: bucket where to upload the folder to
        :param folder: the folder location in the local file system
        :param key: Optional key where the folder is uploaded
        :param skip: Optional list of files to skip
        :param content_types: Optional dictionary mapping suffixes to
            content types
        :return: a coroutine
        """
        uploader = FolderUploader(self, bucket, folder, key, skip,
                                  content_types)
        return uploader.start()