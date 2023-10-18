def decode(input, output, encoding):
    """Decode common content-transfer-encodings (base64, quopri, uuencode)."""
    if encoding == 'base64':
        import base64
        return base64.decode(input, output)
    if encoding == 'quoted-printable':
        import quopri
        return quopri.decode(input, output)
    if encoding in ('uuencode', 'x-uuencode', 'uue', 'x-uue'):
        import uu
        return uu.decode(input, output)
    if encoding in ('7bit', '8bit'):
        return output.write(input.read())
    if encoding in decodetab:
        pipethrough(input, decodetab[encoding], output)
    else:
        raise ValueError, \
              'unknown Content-Transfer-Encoding: %s' % encoding