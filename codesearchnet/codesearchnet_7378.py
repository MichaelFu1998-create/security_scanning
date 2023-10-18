def ib64_patched(self, attrsD, contentparams):
    """ Patch isBase64 to prevent Base64 encoding of JSON content
    """
    if attrsD.get("mode", "") == "base64":
        return 0
    if self.contentparams["type"].startswith("text/"):
        return 0
    if self.contentparams["type"].endswith("+xml"):
        return 0
    if self.contentparams["type"].endswith("/xml"):
        return 0
    if self.contentparams["type"].endswith("/json"):
        return 0
    return 0