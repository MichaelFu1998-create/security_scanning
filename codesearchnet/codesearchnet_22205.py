def update(dst, src):
    """Recursively update the destination dict-like object with the source dict-like object.

    Useful for merging options and Bunches together!

    Based on:
    http://code.activestate.com/recipes/499335-recursively-update-a-dictionary-without-hitting-py/#c1
    """
    stack = [(dst, src)]

    def isdict(o):
        return hasattr(o, 'keys')

    while stack:
        current_dst, current_src = stack.pop()
        for key in current_src:
            if key not in current_dst:
                current_dst[key] = current_src[key]
            else:
                if isdict(current_src[key]) and isdict(current_dst[key]):
                    stack.append((current_dst[key], current_src[key]))
                else:
                    current_dst[key] = current_src[key]
    return dst