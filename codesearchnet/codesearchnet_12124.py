def list_trilegal_filtersystems():
    '''
    This just lists all the filter systems available for TRILEGAL.

    '''

    print('%-40s %s' % ('FILTER SYSTEM NAME','DESCRIPTION'))
    print('%-40s %s' % ('------------------','-----------'))
    for key in sorted(TRILEGAL_FILTER_SYSTEMS.keys()):
        print('%-40s %s' % (key, TRILEGAL_FILTER_SYSTEMS[key]['desc']))