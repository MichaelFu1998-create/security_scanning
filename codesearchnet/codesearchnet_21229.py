def color(teffs):
    """
    Conventional color descriptions of stars.
    Source: https://en.wikipedia.org/wiki/Stellar_classification
    """
    colors = []
    for t in teffs:
        if t >= 7500:
            colors.append('blue_white')  # RGB:CAE1FF
        elif t >= 6000:
            colors.append('white')  # RGB:F6F6F6
        elif t >= 5200:
            colors.append('yellowish_white')  # RGB:FFFEB2
        elif t >= 3700:
            colors.append('pale_yellow_orange')  # RGB:FFB28B
        else:
            colors.append('light_orange_red')  # RGB:FF9966
    return colors