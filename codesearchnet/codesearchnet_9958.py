def _calculate_aes_cipher(key):
    """
    Determines if the key is a valid AES 128, 192 or 256 key

    :param key:
        A byte string of the key to use

    :raises:
        ValueError - when an invalid key is provided

    :return:
        A unicode string of the AES variation - "aes128", "aes192" or "aes256"
    """

    if len(key) not in [16, 24, 32]:
        raise ValueError(pretty_message(
            '''
            key must be either 16, 24 or 32 bytes (128, 192 or 256 bits)
            long - is %s
            ''',
            len(key)
        ))

    if len(key) == 16:
        cipher = 'aes128'
    elif len(key) == 24:
        cipher = 'aes192'
    elif len(key) == 32:
        cipher = 'aes256'

    return cipher