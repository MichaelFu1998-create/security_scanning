def create_feature_array(text, n_pad=21):
    """
    Create feature array of character and surrounding characters
    """
    n = len(text)
    n_pad_2 = int((n_pad - 1)/2)
    text_pad = [' '] * n_pad_2  + [t for t in text] + [' '] * n_pad_2
    x_char, x_type = [], []
    for i in range(n_pad_2, n_pad_2 + n):
        char_list = text_pad[i + 1: i + n_pad_2 + 1] + \
                    list(reversed(text_pad[i - n_pad_2: i])) + \
                    [text_pad[i]]
        char_map = [CHARS_MAP.get(c, 80) for c in char_list]
        char_type = [CHAR_TYPES_MAP.get(CHAR_TYPE_FLATTEN.get(c, 'o'), 4)
                     for c in char_list]
        x_char.append(char_map)
        x_type.append(char_type)
    x_char = np.array(x_char).astype(float)
    x_type = np.array(x_type).astype(float)
    return x_char, x_type