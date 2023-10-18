def list_namespaces():
    '''Print out a listing of available namespaces'''
    print('{:30s}\t{:40s}'.format('NAME', 'DESCRIPTION'))
    print('-' * 78)
    for sch in sorted(__NAMESPACE__):
        desc = __NAMESPACE__[sch]['description']
        desc = (desc[:44] + '..') if len(desc) > 46 else desc
        print('{:30s}\t{:40s}'.format(sch, desc))