def get_iptc_data(filename):
    """Return a dict with the raw IPTC data."""

    logger = logging.getLogger(__name__)

    iptc_data = {}
    raw_iptc = {}

    # PILs IptcImagePlugin issues a SyntaxError in certain circumstances
    # with malformed metadata, see PIL/IptcImagePlugin.py", line 71.
    # ( https://github.com/python-pillow/Pillow/blob/9dd0348be2751beb2c617e32ff9985aa2f92ae5f/src/PIL/IptcImagePlugin.py#L71 )
    try:
        img = _read_image(filename)
        raw_iptc = IptcImagePlugin.getiptcinfo(img)
    except SyntaxError:
        logger.info('IPTC Error in %s', filename)

    # IPTC fields are catalogued in:
    # https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata
    # 2:05 is the IPTC title property
    if raw_iptc and (2, 5) in raw_iptc:
        iptc_data["title"] = raw_iptc[(2, 5)].decode('utf-8', errors='replace')

    # 2:120 is the IPTC description property
    if raw_iptc and (2, 120) in raw_iptc:
        iptc_data["description"] = raw_iptc[(2, 120)].decode('utf-8',
                                                             errors='replace')

    # 2:105 is the IPTC headline property
    if raw_iptc and (2, 105) in raw_iptc:
        iptc_data["headline"] = raw_iptc[(2, 105)].decode('utf-8',
                                                          errors='replace')

    return iptc_data