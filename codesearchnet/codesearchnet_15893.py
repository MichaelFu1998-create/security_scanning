def kill_octave():
    """Kill all octave instances (cross-platform).

    This will restart the "octave" instance.  If you have instantiated
    Any other Oct2Py objects, you must restart them.
    """
    import os
    if os.name == 'nt':
        os.system('taskkill /im octave /f')
    else:
        os.system('killall -9 octave')
        os.system('killall -9 octave-cli')
    octave.restart()