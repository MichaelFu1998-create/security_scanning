def upload(self, dataset_id, source_path, dest_path=None):
        """
        Upload a file, specifying source and dest paths a file (acts as the scp command).asdfasdf

        :param source_path: The path to the file on the source host asdf
        :type source_path: str
        :param dest_path: The path to the file where the contents of the upload will be written (on the dest host)
        :type dest_path: str
        :return: The result of the upload process
        :rtype: :class:`UploadResult`
        """
        upload_result = UploadResult()
        source_path = str(source_path)
        if not dest_path:
            dest_path = source_path
        else:
            dest_path = str(dest_path)
        if os.path.isdir(source_path):
            for path, subdirs, files in os.walk(source_path):
                relative_path = os.path.relpath(path, source_path)
                current_dest_prefix = dest_path
                if relative_path is not ".":
                    current_dest_prefix = os.path.join(current_dest_prefix, relative_path)
                for name in files:
                    current_dest_path = os.path.join(current_dest_prefix, name)
                    current_source_path = os.path.join(path, name)
                    try:
                        if self.upload(dataset_id, current_source_path, current_dest_path).successful():
                            upload_result.add_success(current_source_path)
                        else:
                            upload_result.add_failure(current_source_path,"Upload failure")
                    except (CitrinationClientError, ValueError) as e:
                        upload_result.add_failure(current_source_path, str(e))
            return upload_result
        elif os.path.isfile(source_path):
            file_data = { "dest_path": str(dest_path), "src_path": str(source_path)}
            j = self._get_success_json(self._post_json(routes.upload_to_dataset(dataset_id), data=file_data))
            s3url = _get_s3_presigned_url(j)
            with open(source_path, 'rb') as f:
                if os.stat(source_path).st_size == 0:
                    # Upload a null character as a placeholder for
                    # the empty file since Citrination does not support
                    # truly empty files
                    data = "\0"
                else:
                    data = f
                r = requests.put(s3url, data=data, headers=j["required_headers"])
                if r.status_code == 200:
                    data = {'s3object': j['url']['path'], 's3bucket': j['bucket']}
                    self._post_json(routes.update_file(j['file_id']), data=data)
                    upload_result.add_success(source_path)
                    return upload_result
                else:
                    raise CitrinationClientError("Failure to upload {} to Citrination".format(source_path))
        else:
            raise ValueError("No file at specified path {}".format(source_path))