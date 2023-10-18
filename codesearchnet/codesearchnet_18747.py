def cleaned_sites():
    """
    Create a list of tuples mapping domains from the sites table to their
    site name.  The domains will be cleaned into regexes that may be
    more permissive than the site domain is in the db.
    
    [(domain_regex, domain_name, domain_string), ...]
    """
    mappings = {}
    for site in Site.objects.all():
        # match the site domain, breaking it into several pieces
        match = re.match(r'(https?://)?(www[^\.]*\.)?([^/]+)', site.domain)
        
        if match is not None:
            http, www, domain = match.groups()
            
            # if the protocol is specified, use it, otherwise accept 80/443
            http_re = http or r'https?:\/\/'
            
            # whether or not there's a www (or www2 :x) allow it in the match
            www_re = r'(?:www[^\.]*\.)?'
            
            # build a regex of the permissive http re, the www re, and the domain
            domain_re = http_re + www_re + domain
            
            # now build a pretty string representation of the domain
            http = http or r'http://'
            www = www or ''
            normalized = http + www + domain
            
            mappings[site.pk] = (domain_re, site.name, normalized)
    return mappings