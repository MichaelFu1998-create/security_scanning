def _advapi32_create_blob(key_info, key_type, algo, signing=True):
    """
    Generates a blob for importing a key to CryptoAPI

    :param key_info:
        An asn1crypto.keys.PublicKeyInfo or asn1crypto.keys.PrivateKeyInfo
        object

    :param key_type:
        A unicode string of "public" or "private"

    :param algo:
        A unicode string of "rsa" or "dsa"

    :param signing:
        If the key handle is for signing - may only be False for rsa keys

    :return:
        A byte string of a blob to pass to advapi32.CryptImportKey()
    """

    if key_type == 'public':
        blob_type = Advapi32Const.PUBLICKEYBLOB
    else:
        blob_type = Advapi32Const.PRIVATEKEYBLOB

    if algo == 'rsa':
        struct_type = 'RSABLOBHEADER'
        if signing:
            algorithm_id = Advapi32Const.CALG_RSA_SIGN
        else:
            algorithm_id = Advapi32Const.CALG_RSA_KEYX
    else:
        struct_type = 'DSSBLOBHEADER'
        algorithm_id = Advapi32Const.CALG_DSS_SIGN

    blob_header_pointer = struct(advapi32, 'BLOBHEADER')
    blob_header = unwrap(blob_header_pointer)
    blob_header.bType = blob_type
    blob_header.bVersion = Advapi32Const.CUR_BLOB_VERSION
    blob_header.reserved = 0
    blob_header.aiKeyAlg = algorithm_id

    blob_struct_pointer = struct(advapi32, struct_type)
    blob_struct = unwrap(blob_struct_pointer)
    blob_struct.publickeystruc = blob_header

    bit_size = key_info.bit_size
    len1 = bit_size // 8
    len2 = bit_size // 16

    if algo == 'rsa':
        pubkey_pointer = struct(advapi32, 'RSAPUBKEY')
        pubkey = unwrap(pubkey_pointer)
        pubkey.bitlen = bit_size
        if key_type == 'public':
            parsed_key_info = key_info['public_key'].parsed
            pubkey.magic = Advapi32Const.RSA1
            pubkey.pubexp = parsed_key_info['public_exponent'].native
            blob_data = int_to_bytes(parsed_key_info['modulus'].native, signed=False, width=len1)[::-1]
        else:
            parsed_key_info = key_info['private_key'].parsed
            pubkey.magic = Advapi32Const.RSA2
            pubkey.pubexp = parsed_key_info['public_exponent'].native
            blob_data = int_to_bytes(parsed_key_info['modulus'].native, signed=False, width=len1)[::-1]
            blob_data += int_to_bytes(parsed_key_info['prime1'].native, signed=False, width=len2)[::-1]
            blob_data += int_to_bytes(parsed_key_info['prime2'].native, signed=False, width=len2)[::-1]
            blob_data += int_to_bytes(parsed_key_info['exponent1'].native, signed=False, width=len2)[::-1]
            blob_data += int_to_bytes(parsed_key_info['exponent2'].native, signed=False, width=len2)[::-1]
            blob_data += int_to_bytes(parsed_key_info['coefficient'].native, signed=False, width=len2)[::-1]
            blob_data += int_to_bytes(parsed_key_info['private_exponent'].native, signed=False, width=len1)[::-1]
        blob_struct.rsapubkey = pubkey

    else:
        pubkey_pointer = struct(advapi32, 'DSSPUBKEY')
        pubkey = unwrap(pubkey_pointer)
        pubkey.bitlen = bit_size

        if key_type == 'public':
            pubkey.magic = Advapi32Const.DSS1
            params = key_info['algorithm']['parameters'].native
            key_data = int_to_bytes(key_info['public_key'].parsed.native, signed=False, width=len1)[::-1]
        else:
            pubkey.magic = Advapi32Const.DSS2
            params = key_info['private_key_algorithm']['parameters'].native
            key_data = int_to_bytes(key_info['private_key'].parsed.native, signed=False, width=20)[::-1]
        blob_struct.dsspubkey = pubkey

        blob_data = int_to_bytes(params['p'], signed=False, width=len1)[::-1]
        blob_data += int_to_bytes(params['q'], signed=False, width=20)[::-1]
        blob_data += int_to_bytes(params['g'], signed=False, width=len1)[::-1]
        blob_data += key_data

        dssseed_pointer = struct(advapi32, 'DSSSEED')
        dssseed = unwrap(dssseed_pointer)
        # This indicates no counter or seed info is available
        dssseed.counter = 0xffffffff

        blob_data += struct_bytes(dssseed_pointer)

    return struct_bytes(blob_struct_pointer) + blob_data