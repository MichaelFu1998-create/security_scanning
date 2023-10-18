def colormagdiagram_cpdir(
        cpdir,
        outpkl,
        cpfileglob='checkplot*.pkl*',
        color_mag1=['gaiamag','sdssg'],
        color_mag2=['kmag','kmag'],
        yaxis_mag=['gaia_absmag','rpmj']
):
    '''This makes CMDs for all checkplot pickles in the provided directory.

    Can make an arbitrary number of CMDs given lists of x-axis colors and y-axis
    mags to use.

    Parameters
    ----------

    cpdir : list of str
        This is the directory to get the list of input checkplot pickles from.

    outpkl : str
        The filename of the output pickle that will contain the color-mag
        information for all objects in the checkplots specified in `cplist`.

    cpfileglob : str
        The UNIX fileglob to use to search for checkplot pickle files.

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
        in the input checkplot directory.

    Notes
    -----

    This can make many CMDs in one go. For example, the default kwargs for
    `color_mag`, `color_mag2`, and `yaxis_mag` result in two CMDs generated and
    written to the output pickle file:

    - CMD1 -> gaiamag - kmag on the x-axis vs gaia_absmag on the y-axis
    - CMD2 -> sdssg - kmag on the x-axis vs rpmj (J reduced PM) on the y-axis

    '''

    cplist = glob.glob(os.path.join(cpdir, cpfileglob))

    return colormagdiagram_cplist(cplist,
                                  outpkl,
                                  color_mag1=color_mag1,
                                  color_mag2=color_mag2,
                                  yaxis_mag=yaxis_mag)