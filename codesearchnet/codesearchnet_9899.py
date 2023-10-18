def _parse_dict(stream):
    """Parse dictionary, with optional starting character '{'
    return (tuple):
        Number of characters parsed from to_parse
        Parsed dictionary
    """
    obj = {}

    logger.debug("%s", fmt_green("parsing dict"))

    while True:
        c = stream.read(1)
        if c in _WHITESPACE:
            pass
        elif c in ["{", ","]:
            pass
        elif c in ["}", ""]:
            # end of object, exit loop
            break

        else:
            stream.seek(-1)
            key, val = _parse_key_val(stream)
            if key in obj:
                # This is a gdb bug. We should never get repeated keys in a dict!
                # See https://sourceware.org/bugzilla/show_bug.cgi?id=22217
                # and https://github.com/cs01/pygdbmi/issues/19
                # Example:
                #   thread-ids={thread-id="1",thread-id="2"}
                # Results in:
                #   thread-ids: {{'thread-id': ['1', '2']}}
                # Rather than the lossy
                #   thread-ids: {'thread-id': 2}  # '1' got overwritten!
                if isinstance(obj[key], list):
                    obj[key].append(val)
                else:
                    obj[key] = [obj[key], val]
            else:
                obj[key] = val

            look_ahead_for_garbage = True
            c = stream.read(1)
            while look_ahead_for_garbage:
                if c in ["}", ",", ""]:
                    look_ahead_for_garbage = False
                else:
                    # got some garbage text, skip it. for example:
                    # name="gdb"gargage  # skip over 'garbage'
                    # name="gdb"\n  # skip over '\n'
                    logger.debug("skipping unexpected charcter: " + c)
                    c = stream.read(1)
            stream.seek(-1)

    logger.debug("parsed dict")
    logger.debug("%s", fmt_green(obj))
    return obj