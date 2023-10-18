def parse_comment_telemetry(text):
    """
    Looks for base91 telemetry found in comment field
    Returns [remaining_text, telemetry]
    """
    parsed = {}
    match = re.findall(r"^(.*?)\|([!-{]{4,14})\|(.*)$", text)

    if match and len(match[0][1]) % 2 == 0:
        text, telemetry, post = match[0]
        text += post

        temp = [0] * 7
        for i in range(7):
            temp[i] = base91.to_decimal(telemetry[i*2:i*2+2])

        parsed.update({
            'telemetry': {
                'seq': temp[0],
                'vals': temp[1:6]
                }
            })

        if temp[6] != '':
            parsed['telemetry'].update({
                'bits': "{0:08b}".format(temp[6] & 0xFF)[::-1]
                })

    return (text, parsed)