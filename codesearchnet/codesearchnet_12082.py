def colormagdiagram_cplist(cplist,
                           outpkl,
                           color_mag1=['gaiamag','sdssg'],
                           color_mag2=['kmag','kmag'],
                           yaxis_mag=['gaia_absmag','rpmj']):
    '''This makes color-mag diagrams for all checkplot pickles in the provided
    list.

    Can make an arbitrary number of CMDs given lists of x-axis colors and y-axis
    mags to use.

    Parameters
    ----------

    cplist : list of str
        This is the list of checkplot pickles to process.

    outpkl : str
        The filename of the output pickle that will contain the color-mag
        information for all objects in the checkplots specified in `cplist`.

    color_mag1 : list of str
        This a list of the keys in each checkplot's `objectinfo` dict that will
        be used as color_1 in the equation::

                x-axis color = color_mag1 - color_mag2

    color_mag2 : list of str
        This a list of the keys in each checkplot's `objectinfo` dict that will
        be used as color_2 in the equation::

                x-axis color = color_mag1 - color_mag2

    yaxis_mag : list of str
        This is a list of the keys in each checkplot's `objectinfo` dict that
        will be used as the (absolute) magnitude y-axis of the color-mag
        diagrams.

    Returns
    -------

    str
        The path to the generated CMD pickle file for the collection of objects
        in the input checkplot list.

    Notes
    -----

    This can make many CMDs in one go. For example, the default kwargs for
    `color_mag`, `color_mag2`, and `yaxis_mag` result in two CMDs generated and
    written to the output pickle file:

    - CMD1 -> gaiamag - kmag on the x-axis vs gaia_absmag on the y-axis
    - CMD2 -> sdssg - kmag on the x-axis vs rpmj (J reduced PM) on the y-axis

    '''

    # first, we'll collect all of the info
    cplist_objectids = []
    cplist_mags = []
    cplist_colors = []

    for cpf in cplist:

        cpd = _read_checkplot_picklefile(cpf)
        cplist_objectids.append(cpd['objectid'])

        thiscp_mags = []
        thiscp_colors = []

        for cm1, cm2, ym in zip(color_mag1, color_mag2, yaxis_mag):

            if (ym in cpd['objectinfo'] and
                cpd['objectinfo'][ym] is not None):
                thiscp_mags.append(cpd['objectinfo'][ym])
            else:
                thiscp_mags.append(np.nan)

            if (cm1 in cpd['objectinfo'] and
                cpd['objectinfo'][cm1] is not None and
                cm2 in cpd['objectinfo'] and
                cpd['objectinfo'][cm2] is not None):
                thiscp_colors.append(cpd['objectinfo'][cm1] -
                                     cpd['objectinfo'][cm2])
            else:
                thiscp_colors.append(np.nan)

        cplist_mags.append(thiscp_mags)
        cplist_colors.append(thiscp_colors)


    # convert these to arrays
    cplist_objectids = np.array(cplist_objectids)
    cplist_mags = np.array(cplist_mags)
    cplist_colors = np.array(cplist_colors)

    # prepare the outdict
    cmddict = {'objectids':cplist_objectids,
               'mags':cplist_mags,
               'colors':cplist_colors,
               'color_mag1':color_mag1,
               'color_mag2':color_mag2,
               'yaxis_mag':yaxis_mag}

    # save the pickled figure and dict for fast retrieval later
    with open(outpkl,'wb') as outfd:
        pickle.dump(cmddict, outfd, pickle.HIGHEST_PROTOCOL)

    plt.close('all')

    return cmddict