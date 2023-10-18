def decode(enc):
    '''Decode a base58 string (ex: a Monero address) into hexidecimal form.'''
    enc = bytearray(enc, encoding='ascii')
    l_enc = len(enc)

    if l_enc == 0:
        return ""

    full_block_count = l_enc // __fullEncodedBlockSize
    last_block_size = l_enc % __fullEncodedBlockSize
    try:
        last_block_decoded_size = __encodedBlockSizes.index(last_block_size)
    except ValueError:
        raise ValueError("Invalid encoded length: %d" % l_enc)

    data_size = full_block_count * __fullBlockSize + last_block_decoded_size

    data = bytearray(data_size)
    for i in range(full_block_count):
        data = decode_block(enc[(i*__fullEncodedBlockSize):(i*__fullEncodedBlockSize+__fullEncodedBlockSize)], data, i * __fullBlockSize)

    if last_block_size > 0:
        data = decode_block(enc[(full_block_count*__fullEncodedBlockSize):(full_block_count*__fullEncodedBlockSize+last_block_size)], data, full_block_count * __fullBlockSize)

    return _binToHex(data)