def urlsafe_nopadding_b64decode(data):
    '''URL safe Base64 decode without padding (=)'''

    padding = len(data) % 4
    if padding != 0:
        padding = 4 - padding
    padding = '=' * padding
    data = data + padding
    return urlsafe_b64decode(data)