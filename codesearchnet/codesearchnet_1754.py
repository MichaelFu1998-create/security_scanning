def encode(input, output, encoding):
    """Encode common content-transfer-encodings (base64, quopri, uuencode)."""
    if encoding == 'base64':
        import base64
        return base64.encode(input, output)
    if encoding == 'quoted-printable':
        import quopri
        return quopri.encode(input, output, 0)
    if encoding in ('uuencode', 'x-uuencode', 'uue', 'x-uue'):
        import uu
        return uu.encode(input, output)
    if encoding in ('7bit', '8bit'):
        return output.write(input.read())
    if encoding in encodetab:
        pipethrough(input, encodetab[encoding], output)
    else:
        raise ValueError, \
              'unknown Content-Transfer-Encoding: %s' % encoding