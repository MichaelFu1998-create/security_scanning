def load_savefile(input_file, layers=0, verbose=False, lazy=False):
    """
    Parse a savefile as a pcap_savefile instance. Returns the savefile
    on success and None on failure. Verbose mode prints additional information
    about the file's processing. layers defines how many layers to descend and
    decode the packet. input_file should be a Python file object.
    """
    global VERBOSE
    old_verbose = VERBOSE
    VERBOSE = verbose

    __TRACE__('[+] attempting to load {:s}', (input_file.name,))

    header = _load_savefile_header(input_file)
    if __validate_header__(header):
        __TRACE__('[+] found valid header')
        if lazy:
            packets = _generate_packets(input_file, header, layers)
            __TRACE__('[+] created packet generator')
        else:
            packets = _load_packets(input_file, header, layers)
            __TRACE__('[+] loaded {:d} packets', (len(packets),))
        sfile = pcap_savefile(header, packets)
        __TRACE__('[+] finished loading savefile.')
    else:
        __TRACE__('[!] invalid savefile')
        sfile = None

    VERBOSE = old_verbose
    return sfile