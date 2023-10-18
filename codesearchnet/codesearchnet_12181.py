def cp2png(checkplotin, extrarows=None):
    '''This is just a shortened form of the function above for convenience.

    This only handles pickle files as input.

    Parameters
    ----------

    checkplotin : str
        File name of a checkplot pickle file to convert to a PNG.

    extrarows : list of tuples
        This is a list of 4-element tuples containing paths to PNG files that
        will be added to the end of the rows generated from the checkplotin
        pickle/dict. Each tuple represents a row in the final output PNG
        file. If there are less than 4 elements per tuple, the missing elements
        will be filled in with white-space. If there are more than 4 elements
        per tuple, only the first four will be used.

        The purpose of this kwarg is to incorporate periodograms and phased LC
        plots (in the form of PNGs) generated from an external period-finding
        function or program (like VARTOOLS) to allow for comparison with
        astrobase results.

        NOTE: the PNG files specified in `extrarows` here will be added to those
        already present in the input `checkplotdict['externalplots']` if that is
        None because you passed in a similar list of external plots to the
        :py:func:`astrobase.checkplot.pkl.checkplot_pickle` function earlier. In
        this case, `extrarows` can be used to add even more external plots if
        desired.

        Each external plot PNG will be resized to 750 x 480 pixels to fit into
        an output image cell.

        By convention, each 4-element tuple should contain:

        - a periodiogram PNG
        - phased LC PNG with 1st best peak period from periodogram
        - phased LC PNG with 2nd best peak period from periodogram
        - phased LC PNG with 3rd best peak period from periodogram

        Example of extrarows::

            [('/path/to/external/bls-periodogram.png',
              '/path/to/external/bls-phasedlc-plot-bestpeak.png',
              '/path/to/external/bls-phasedlc-plot-peak2.png',
              '/path/to/external/bls-phasedlc-plot-peak3.png'),
             ('/path/to/external/pdm-periodogram.png',
              '/path/to/external/pdm-phasedlc-plot-bestpeak.png',
              '/path/to/external/pdm-phasedlc-plot-peak2.png',
              '/path/to/external/pdm-phasedlc-plot-peak3.png'),
            ...]

    Returns
    -------

    str
        The absolute path to the generated checkplot PNG.

    '''

    if checkplotin.endswith('.gz'):
        outfile = checkplotin.replace('.pkl.gz','.png')
    else:
        outfile = checkplotin.replace('.pkl','.png')

    return checkplot_pickle_to_png(checkplotin, outfile, extrarows=extrarows)