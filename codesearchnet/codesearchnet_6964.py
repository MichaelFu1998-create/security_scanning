def Carcinogen(CASRN, AvailableMethods=False, Method=None):
    r'''Looks up if a chemical is listed as a carcinogen or not according to
    either a specifc method or with all methods.

    Returns either the status as a string for a specified method, or the
    status of the chemical in all available data sources, in the format
    {source: status}.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    status : str or dict
        Carcinogen status information [-]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain carcinogen status with the
        given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Carcinogen_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        if a chemical is listed as carcinogenic, and will return methods
        instead of the status

    Notes
    -----
    Supported methods are:

        * **IARC**: International Agency for Research on Cancer, [1]_. As
          extracted with a last update of  February 22, 2016. Has listing
          information of 843 chemicals with CAS numbers. Chemicals without
          CAS numbers not included here. If two listings for the same CAS
          were available, that closest to the CAS number was used. If two
          listings were available published at different times, the latest
          value was used. All else equal, the most pessimistic value was used.
        * **NTP**: National Toxicology Program, [2]_. Has data on 226
          chemicals.

    Examples
    --------
    >>> Carcinogen('61-82-5')
    {'National Toxicology Program 13th Report on Carcinogens': 'Reasonably Anticipated', 'International Agency for Research on Cancer': 'Not classifiable as to its carcinogenicity to humans (3)'}

    References
    ----------
    .. [1] International Agency for Research on Cancer. Agents Classified by
       the IARC Monographs, Volumes 1-115. Lyon, France: IARC; 2016 Available
       from: http://monographs.iarc.fr/ENG/Classification/
    .. [2] NTP (National Toxicology Program). 2014. Report on Carcinogens,
       Thirteenth Edition. Research Triangle Park, NC: U.S. Department of
       Health and Human Services, Public Health Service.
       http://ntp.niehs.nih.gov/pubhealth/roc/roc13/
    '''
    methods = [COMBINED, IARC, NTP]
    if AvailableMethods:
        return methods
    if not Method:
        Method = methods[0]
    if Method == IARC:
        if CASRN in IARC_data.index:
            status = IARC_codes[IARC_data.at[CASRN, 'group']]
        else:
            status = UNLISTED
    elif Method == NTP:
        if CASRN in NTP_data.index:
            status = NTP_codes[NTP_data.at[CASRN, 'Listing']]
        else:
            status = UNLISTED
    elif Method == COMBINED:
        status = {}
        for method in methods[1:]:
            status[method] = Carcinogen(CASRN, Method=method)
    else:
        raise Exception('Failure in in function')
    return status