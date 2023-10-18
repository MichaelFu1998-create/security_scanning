def encrypt(password='password', salt=None):
    """
    Return SHA1 hexdigest of a password (optionally salted with a string).


    """
    if not salt:
        salt = str(datetime.utcnow())

    try:
        #  available for python 2.7.8 and python 3.4+
        dk = hashlib.pbkdf2_hmac('sha1', password.encode(), salt.encode(), 100000)
        hexdigest = binascii.hexlify(dk).decode('utf-8')
    except AttributeError:
        # see https://pymotw.com/2/hashlib/
        # see https://docs.python.org/release/2.5/lib/module-hashlib.html
        dk = hashlib.sha1()
        dk.update(password.encode() + salt.encode())
        hexdigest = dk.hexdigest()
    return hexdigest