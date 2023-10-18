def generate_hatpi_binnedlc_pkl(binnedpklf, textlcf, timebinsec,
                                outfile=None):
    '''
    This reads the binned LC and writes it out to a pickle.

    '''

    binlcdict = read_hatpi_binnedlc(binnedpklf, textlcf, timebinsec)

    if binlcdict:
        if outfile is None:
            outfile = os.path.join(
                os.path.dirname(binnedpklf),
                '%s-hplc.pkl' % (
                    os.path.basename(binnedpklf).replace('sec-lc.pkl.gz','')
                )
            )

        return lcdict_to_pickle(binlcdict, outfile=outfile)
    else:
        LOGERROR('could not read binned HATPI LC: %s' % binnedpklf)
        return None