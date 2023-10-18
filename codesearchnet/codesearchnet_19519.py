def color_from_hex(value):
    """ Takes an HTML hex code
        and converts it to a proper hue value """
    if "#" in value:
        value = value[1:]
    
    try:
        unhexed = bytes.fromhex(value)
    except:
        unhexed = binascii.unhexlify(value) # Fallback for 2.7 compatibility
    return color_from_rgb(*struct.unpack('BBB',unhexed))