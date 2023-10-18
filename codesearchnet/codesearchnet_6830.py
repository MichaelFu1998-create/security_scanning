def legal_status(CASRN, Method=None, AvailableMethods=False, CASi=None):
    r'''Looks up the legal status of a chemical according to either a specifc
    method or with all methods.

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
        Legal status information [-]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain legal status with the
        given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        legal_status_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        the legal status for the desired chemical, and will return methods
        instead of the status
    CASi : int, optional
        CASRN as an integer, used internally [-]

    Notes
    -----

    Supported methods are:

        * **DSL**: Canada Domestic Substance List, [1]_. As extracted on Feb 11, 2015
          from a html list. This list is updated continuously, so this version
          will always be somewhat old. Strictly speaking, there are multiple
          lists but they are all bundled together here. A chemical may be
          'Listed', or be on the 'Non-Domestic Substances List (NDSL)',
          or be on the list of substances with 'Significant New Activity (SNAc)',
          or be on the DSL but with a 'Ministerial Condition pertaining to this
          substance', or have been removed from the DSL, or have had a
          Ministerial prohibition for the substance.
        * **TSCA**: USA EPA Toxic Substances Control Act Chemical Inventory, [2]_.
          This list is as extracted on 2016-01. It is believed this list is
          updated on a periodic basis (> 6 month). A chemical may simply be
          'Listed', or may have certain flags attached to it. All these flags
          are described in the dict TSCA_flags.
        * **EINECS**: European INventory of Existing Commercial chemical
          Substances, [3]_. As extracted from a spreadsheet dynamically
          generated at [1]_. This list was obtained March 2015; a more recent
          revision already exists.
        * **NLP**: No Longer Polymers, a list of chemicals with special
          regulatory exemptions in EINECS. Also described at [3]_.
        * **SPIN**: Substances Prepared in Nordic Countries. Also a boolean
          data type. Retrieved 2015-03 from [4]_.

    Other methods which could be added are:

        * Australia: AICS Australian Inventory of Chemical Substances
        * China: Inventory of Existing Chemical Substances Produced or Imported
          in China (IECSC)
        * Europe: REACH List of Registered Substances
        * India: List of Hazardous Chemicals
        * Japan: ENCS: Inventory of existing and new chemical substances
        * Korea: Existing Chemicals Inventory (KECI)
        * Mexico: INSQ National Inventory of Chemical Substances in Mexico
        * New Zealand:  Inventory of Chemicals (NZIoC)
        * Philippines: PICCS Philippines Inventory of Chemicals and Chemical
          Substances

    Examples
    --------
    >>> pprint(legal_status('64-17-5'))
    {'DSL': 'LISTED',
     'EINECS': 'LISTED',
     'NLP': 'UNLISTED',
     'SPIN': 'LISTED',
     'TSCA': 'LISTED'}

    References
    ----------
    .. [1] Government of Canada.. "Substances Lists" Feb 11, 2015.
       https://www.ec.gc.ca/subsnouvelles-newsubs/default.asp?n=47F768FE-1.
    .. [2] US EPA. "TSCA Chemical Substance Inventory." Accessed April 2016.
       https://www.epa.gov/tsca-inventory.
    .. [3] ECHA. "EC Inventory". Accessed March 2015.
       http://echa.europa.eu/information-on-chemicals/ec-inventory.
    .. [4] SPIN. "SPIN Substances in Products In Nordic Countries." Accessed
       March 2015. http://195.215.202.233/DotNetNuke/default.aspx.
    '''
    load_law_data()
    if not CASi:
        CASi = CAS2int(CASRN)
    methods = [COMBINED, DSL, TSCA, EINECS, NLP, SPIN]
    if AvailableMethods:
        return methods
    if not Method:
        Method = methods[0]
    if Method == DSL:
        if CASi in DSL_data.index:
            status = CAN_DSL_flags[DSL_data.at[CASi, 'Registry']]
        else:
            status = UNLISTED
    elif Method == TSCA:
        if CASi in TSCA_data.index:
            data = TSCA_data.loc[CASi].to_dict()
            if any(data.values()):
                status = sorted([TSCA_flags[i] for i in data.keys() if data[i]])
            else:
                status = LISTED
        else:
            status = UNLISTED
    elif Method == EINECS:
        if CASi in EINECS_data.index:
            status = LISTED
        else:
            status = UNLISTED
    elif Method == NLP:
        if CASi in NLP_data.index:
            status = LISTED
        else:
            status = UNLISTED
    elif Method == SPIN:
        if CASi in SPIN_data.index:
            status = LISTED
        else:
            status = UNLISTED
    elif Method == COMBINED:
        status = {}
        for method in methods[1:]:
            status[method] = legal_status(CASRN, Method=method, CASi=CASi)
    else:
        raise Exception('Failure in in function')
    return status