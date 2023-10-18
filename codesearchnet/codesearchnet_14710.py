def operation_file(uploader, cmd, filename=''):
    """File operations"""
    if cmd == 'list':
        operation_list(uploader)
    if cmd == 'do':
        for path in filename:
            uploader.file_do(path)
    elif cmd == 'format':
        uploader.file_format()
    elif cmd == 'remove':
        for path in filename:
            uploader.file_remove(path)
    elif cmd == 'print':
        for path in filename:
            uploader.file_print(path)