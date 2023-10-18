def color_from_hls(hue, light, sat):
    """ Takes a hls color and converts to proper hue 
        Bulbs use a BGR order instead of RGB """
    if light > 0.95: #too bright, let's just switch to white
        return 256
    elif light < 0.05: #too dark, let's shut it off
        return -1
    else:
        hue = (-hue + 1 + 2.0/3.0) % 1 # invert and translate by 2/3
        return int(floor(hue * 256))