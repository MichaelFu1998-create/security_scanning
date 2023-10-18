def getLogin(filename, user, passwd):
    '''
    write user/passwd to login file or get them from file.
    This method is not Py3 safe (byte vs. str)
    '''
    if filename is None:
        return (user, passwd)
    isPy2 = sys.version_info[0] == 2
    if os.path.exists(filename):
        print("Using file {} for Login".format(filename))
        with open(filename, "r") as loginfile:
            encoded_cred = loginfile.read()
            print("encoded: {}".format(encoded_cred))
            if isPy2:
                decoded_cred = b64decode(encoded_cred)
            else:
                decoded_cred = b64decode(encoded_cred).decode('utf-8')
            login = decoded_cred.split(':', 1)
            return (login[0], login[1])
    else:
        if user is None or passwd is None:
            raise ValueError("user and password must not be None")
        print("Writing file {} for Login".format(filename))
        with open(filename, "wb") as loginfile:
            creds = user+":"+passwd
            if isPy2:
                encoded_cred = b64encode(creds)
            else:
                encoded_cred = b64encode(creds.encode('utf-8'))
            print("encoded: {}".format(encoded_cred))
            loginfile.write(encoded_cred)
        return (user, passwd)