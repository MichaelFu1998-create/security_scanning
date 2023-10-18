def encrypt_files(selected_host, only_link, file_name):
    """
    Encrypts file with gpg and random generated password
    """
    if ENCRYPTION_DISABLED:
        print('For encryption please install gpg')
        exit()
    passphrase = '%030x' % random.randrange(16**30)
    source_filename = file_name
    cmd = 'gpg --batch --symmetric --cipher-algo AES256 --passphrase-fd 0 ' \
          '--output - {}'.format(source_filename)
    encrypted_output = Popen(shlex.split(cmd), stdout=PIPE, stdin=PIPE, stderr=PIPE)
    encrypted_data = encrypted_output.communicate(passphrase.encode())[0]
    return upload_files(encrypted_data, selected_host, only_link, file_name)+'#'+passphrase