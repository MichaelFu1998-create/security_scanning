def decrypt_files(file_link):
    """
    Decrypts file from entered links
    """
    if ENCRYPTION_DISABLED:
        print('For decryption please install gpg')
        exit()
    try:
        parsed_link = re.findall(r'(.*/(.*))#(.{30})', file_link)[0]
        req = urllib.request.Request(
            parsed_link[0],
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' \
                ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
        )
        #downloads the file using fake useragent
        file_response = urllib.request.urlopen(req)
        file_to_decrypt = file_response.read()
        #decrypts the data using piping to ggp
        decrypt_r, decrypt_w = os.pipe()
        cmd = 'gpg --batch --decrypt --passphrase-fd {}'.format(decrypt_r)
        decrypt_output = Popen(shlex.split(cmd), stdout=PIPE, stdin=PIPE, stderr=PIPE, \
                         pass_fds=(decrypt_r,))
        os.close(decrypt_r)
        open(decrypt_w, 'w').write(parsed_link[2])
        decrypted_data, stderr = decrypt_output.communicate(file_to_decrypt)
        with open(parsed_link[1], 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        return parsed_link[1] + ' is decrypted and saved.'
    except IndexError:
        return 'Please enter valid link.'