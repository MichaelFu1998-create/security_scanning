def _create_bitstream(file_path, local_file, item_id, log_ind=None):
    """
    Create a bitstream in the given item.

    :param file_path: full path to the local file
    :type file_path: string
    :param local_file: name of the local file
    :type local_file: string
    :param log_ind: (optional) any additional message to log upon creation of
        the bitstream
    :type log_ind: None | string
    """
    checksum = _streaming_file_md5(file_path)
    upload_token = session.communicator.generate_upload_token(
        session.token, item_id, local_file, checksum)

    if upload_token != '':
        log_trace = 'Uploading bitstream from {0}'.format(file_path)
        # only need to perform the upload if we haven't uploaded before
        # in this cae, the upload token would not be empty
        session.communicator.perform_upload(
            upload_token, local_file, filepath=file_path, itemid=item_id)
    else:
        log_trace = 'Adding a bitstream link in this item to an existing ' \
                    'bitstream from {0}'.format(file_path)

    if log_ind is not None:
        log_trace += log_ind
    print(log_trace)