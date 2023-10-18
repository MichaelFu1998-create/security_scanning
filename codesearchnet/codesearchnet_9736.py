def print_coords(rows, prefix=''):
    """Print coordinates within a sequence.

    This is only used for debugging.  Printed in a form that can be
    pasted into Python for visualization."""
    lat = [row['lat'] for row in rows]
    lon = [row['lon'] for row in rows]
    print('COORDS'+'-' * 5)
    print("%slat, %slon = %r, %r" % (prefix, prefix, lat, lon))
    print('-'*5)