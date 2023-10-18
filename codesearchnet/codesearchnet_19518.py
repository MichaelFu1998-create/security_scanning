def color_from_rgb(red, green, blue):
    """ Takes your standard rgb color 
        and converts it to a proper hue value """
    
    r = min(red, 255)
    g = min(green, 255)
    b = min(blue, 255)
    if r > 1 or g > 1 or b > 1:
        r = r / 255.0
        g = g / 255.0
        b = b / 255.0

    return color_from_hls(*rgb_to_hls(r,g,b))