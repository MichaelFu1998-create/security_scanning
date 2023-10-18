def encode(hex):
    '''Encode hexadecimal string as base58 (ex: encoding a Monero address).'''
    data = _hexToBin(hex)
    l_data = len(data)

    if l_data == 0:
        return ""

    full_block_count = l_data // __fullBlockSize
    last_block_size = l_data % __fullBlockSize
    res_size = full_block_count * __fullEncodedBlockSize + __encodedBlockSizes[last_block_size]

    res = bytearray([__alphabet[0]] * res_size)

    for i in range(full_block_count):
        res = encode_block(data[(i*__fullBlockSize):(i*__fullBlockSize+__fullBlockSize)], res, i * __fullEncodedBlockSize)

    if last_block_size > 0:
        res = encode_block(data[(full_block_count*__fullBlockSize):(full_block_count*__fullBlockSize+last_block_size)], res, full_block_count * __fullEncodedBlockSize)

    return bytes(res).decode('ascii')