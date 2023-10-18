def serial_ports():
    '''
    Returns
    -------
    pandas.DataFrame
        Table of serial ports that match the USB vendor ID and product ID for
        the `Teensy 3.2`_ board.

    .. Teensy 3.2: https://www.pjrc.com/store/teensy32.html
    '''
    df_comports = sd.comports()
    # Match COM ports with USB vendor ID and product IDs for [Teensy 3.2
    # device][1].
    #
    # [1]: https://www.pjrc.com/store/teensy32.html
    df_teensy_comports = df_comports.loc[df_comports.hardware_id.str
                                         .contains('VID:PID=16c0:0483',
                                                   case=False)]
    return df_teensy_comports