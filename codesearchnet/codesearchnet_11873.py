def show(keyword=''):
    """
    Displays a list of all environment key/value pairs for the current role.
    """
    keyword = keyword.strip().lower()
    max_len = max(len(k) for k in env.iterkeys())
    keyword_found = False
    for k in sorted(env.keys()):
        if keyword and keyword not in k.lower():
            continue
        keyword_found = True
        #print '%s: %s' % (k, env[k])
        print('%s: ' % (k.ljust(max_len),))
        pprint(env[k], indent=4)
    if keyword:
        if not keyword_found:
            print('Keyword "%s" not found.' % keyword)