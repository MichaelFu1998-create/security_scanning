def get_text_fingerprint(text, hash_meth, encoding="utf-8"):  # pragma: no cover
    """
    Use default hash method to return hash value of a piece of string
    default setting use 'utf-8' encoding.
    """
    m = hash_meth()
    m.update(text.encode(encoding))
    return m.hexdigest()