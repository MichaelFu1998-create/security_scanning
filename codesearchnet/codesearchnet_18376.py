def get_metainfo(scriptfile,
                 keywords=['author', 'contact', 'copyright', 'download', 'git', 'subversion', 'version', 'website'],
                 special={},
                 first_line_pattern=r'^(?P<progname>.+)(\s+v(?P<version>\S+))?',
                 keyword_pattern_template=r'^\s*%(pretty)s:\s*(?P<%(keyword)s>\S.+?)\s*$',
                 prettify = lambda kw: kw.capitalize().replace('_', ' ')):
    """Dumb helper for pulling metainfo from a script __doc__ string.
 
    Returns a metainfo dict with command, description, progname and the given 
    keywords (if present).   
    
    This function will only make minimal efforts to succeed. If you need 
    anything else: roll your own.
    
    The docstring needs to be multiline and the closing quotes need to be first 
    on a line, optionally preceeded by whitespace. 
    
    The first non-whitespace line is re.search'ed using first_line_pattern, 
    default e.g (version optional, contains no whitespace): PROGNAME [vVERSION]
    
    The next non-whitespace, non-keyword line is expected to be the program 
    description.

    The following lines are re.search'ed against a keyword:pattern dict which
    is constructed using  
    keyword_pattern % dict(pretty=prettify(keyword), keyword=keyword)
    Default prettify is keyword.capitalize().replace('_', ' '). Example,
    for the keyword "licence" will match the following line:
    License: The MIT license.
    and set the license metainfo to "The MIT license.".
        
    Any keyword:pattern pairs that need special treatment can be supplied with 
    special.
    """
    patterns = dict((kw, re.compile(keyword_pattern_template % dict(pretty=prettify(kw), keyword=kw))) for kw in keywords)
    patterns.update(special)
    metainfo = dict()
    
    if scriptfile[-4:] in ['.pyc', '.pyo']: 
        scriptfile = scriptfile[:-1]
    script = open(scriptfile)
    closer = ''
    for line in script:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line[:3] in ('"""', "'''"):
            closer = line[:3] 
            break
        raise ValueError('file contains no docstring')
    if not line:
        for line in script:
            line = line.strip()
            if line:
                break
    g = re.search(first_line_pattern, line[3:]).groupdict()
    metainfo['progname'] = g['progname']
    if g['version']:
        metainfo['version'] = g['version']
    for line in script:
        if line.strip().startswith(closer):
            break
        for keyword, pattern in patterns.items():
            m = pattern.search(line)
            if m:
                metainfo[keyword] = m.group(keyword)
                break
        if line.strip() and not 'description' in metainfo:
            metainfo['description'] = line.strip()
    return metainfo