def rfc2425encode(name,value,parameters=None,charset="utf-8"):
    """Encodes a vCard field into an RFC2425 line.

    :Parameters:
        - `name`: field type name
        - `value`: field value
        - `parameters`: optional parameters
        - `charset`: encoding of the output and of the `value` (if not
          `unicode`)
    :Types:
        - `name`: `str`
        - `value`: `unicode` or `str`
        - `parameters`: `dict` of `str` -> `str`
        - `charset`: `str`

    :return: the encoded RFC2425 line (possibly folded)
    :returntype: `str`"""
    if not parameters:
        parameters={}
    if type(value) is unicode:
        value=value.replace(u"\r\n",u"\\n")
        value=value.replace(u"\n",u"\\n")
        value=value.replace(u"\r",u"\\n")
        value=value.encode(charset,"replace")
    elif type(value) is not str:
        raise TypeError("Bad type for rfc2425 value")
    elif not valid_string_re.match(value):
        parameters["encoding"]="b"
        value=binascii.b2a_base64(value)

    ret=str(name).lower()
    for k,v in parameters.items():
        ret+=";%s=%s" % (str(k),str(v))
    ret+=":"
    while(len(value)>70):
        ret+=value[:70]+"\r\n "
        value=value[70:]
    ret+=value+"\r\n"
    return ret