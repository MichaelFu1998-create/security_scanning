def regex_find(pattern, content):
    """Find the given 'pattern' in 'content'"""

    find = re.findall(pattern, content)
    if not find:
        cij.err("pattern <%r> is invalid, no matches!" % pattern)
        cij.err("content: %r" % content)
        return ''

    if len(find) >= 2:
        cij.err("pattern <%r> is too simple, matched more than 2!" % pattern)
        cij.err("content: %r" % content)
        return ''

    return find[0]