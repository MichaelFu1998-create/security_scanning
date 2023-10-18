def retrieve_document(file_path, directory='sec_filings'):
    '''
        This function takes a file path beginning with edgar and stores the form in a directory.
        The default directory is sec_filings but can be changed through a keyword argument.
    '''
    ftp = FTP('ftp.sec.gov', timeout=None)
    ftp.login()
    name = file_path.replace('/', '_')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with tempfile.TemporaryFile() as temp:
        ftp.retrbinary('RETR %s' % file_path, temp.write)
        temp.seek(0)
        with open('{}/{}'.format(directory, name), 'w+') as f:
            f.write(temp.read().decode("utf-8"))
        f.closed
        records = temp
        retry = False
    ftp.close()