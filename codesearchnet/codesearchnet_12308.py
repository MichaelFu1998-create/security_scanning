def plot_varind_gridsearch_magbin_results(gridsearch_results):
    '''This plots the gridsearch results from `variable_index_gridsearch_magbin`.

    Parameters
    ----------

    gridsearch_results : dict
        This is the dict produced by `variable_index_gridsearch_magbin` above.

    Returns
    -------

    dict
        The returned dict contains filenames of the recovery rate plots made for
        each variability index. These include plots of the precision, recall,
        and Matthews Correlation Coefficient over each magbin and a heatmap of
        these values over the grid points of the variability index stdev values
        arrays used.

    '''

    # get the result pickle/dict
    if (isinstance(gridsearch_results, str) and
        os.path.exists(gridsearch_results)):

        with open(gridsearch_results,'rb') as infd:
            gridresults = pickle.load(infd)

    elif isinstance(gridsearch_results, dict):

        gridresults = gridsearch_results

    else:
        LOGERROR('could not understand the input '
                 'variable index grid-search result dict/pickle')
        return None



    plotres = {'simbasedir':gridresults['simbasedir']}

    recgrid = gridresults['recovery']
    simbasedir = gridresults['simbasedir']

    for magcol in gridresults['magcols']:

        plotres[magcol] = {'best_stetsonj':[],
                           'best_inveta':[],
                           'best_iqr':[],
                           'magbinmedians':gridresults['magbinmedians']}

        # go through all the magbins
        for magbinind, magbinmedian in enumerate(gridresults['magbinmedians']):

            LOGINFO('plotting results for %s: magbin: %.3f' %
                    (magcol, magbinmedian))

            stet_mcc = np.array(
                [x[magcol]['stet_mcc']
                 for x in recgrid[magbinind]]
            )[::(gridresults['inveta_grid'].size *
                 gridresults['stetson_grid'].size)]
            stet_precision = np.array(
                [x[magcol]['stet_precision']
                 for x in recgrid[magbinind]]
            )[::(gridresults['inveta_grid'].size *
                 gridresults['stetson_grid'].size)]
            stet_recall = np.array(
                [x[magcol]['stet_recall']
                 for x in recgrid[magbinind]]
            )[::(gridresults['inveta_grid'].size *
                 gridresults['stetson_grid'].size)]
            stet_missed_inveta_found = np.array(
                [x[magcol]['stet_missed_inveta_found']
                 for x in recgrid[magbinind]]
            )[::(gridresults['inveta_grid'].size *
                 gridresults['stetson_grid'].size)]
            stet_missed_iqr_found = np.array(
                [x[magcol]['stet_missed_iqr_found']
                 for x in recgrid[magbinind]]
            )[::(gridresults['inveta_grid'].size *
                 gridresults['stetson_grid'].size)]

            inveta_mcc = np.array(
                [x[magcol]['inveta_mcc']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    ::gridresults['inveta_grid'].size
                ]
            inveta_precision = np.array(
                [x[magcol]['inveta_precision']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    ::gridresults['inveta_grid'].size
                ]
            inveta_recall = np.array(
                [x[magcol]['inveta_recall']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    ::gridresults['inveta_grid'].size
                ]
            inveta_missed_stet_found = np.array(
                [x[magcol]['inveta_missed_stet_found']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    ::gridresults['inveta_grid'].size
                ]
            inveta_missed_iqr_found = np.array(
                [x[magcol]['inveta_missed_iqr_found']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    ::gridresults['inveta_grid'].size
                ]

            iqr_mcc = np.array(
                [x[magcol]['iqr_mcc']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    :gridresults['inveta_grid'].size
                ]
            iqr_precision = np.array(
                [x[magcol]['iqr_precision']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    :gridresults['inveta_grid'].size
                ]
            iqr_recall = np.array(
                [x[magcol]['iqr_recall']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    :gridresults['inveta_grid'].size
                ]
            iqr_missed_stet_found = np.array(
                [x[magcol]['iqr_missed_stet_found']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    :gridresults['inveta_grid'].size
                ]
            iqr_missed_inveta_found = np.array(
                [x[magcol]['iqr_missed_inveta_found']
                 for x in recgrid[magbinind]]
            )[:(gridresults['iqr_grid'].size *
                gridresults['stetson_grid'].size)][
                    :gridresults['inveta_grid'].size
                ]


            fig = plt.figure(figsize=(6.4*5, 4.8*3))

            # FIRST ROW: stetson J plot

            plt.subplot(3,5,1)
            if np.any(np.isfinite(stet_mcc)):
                plt.plot(gridresults['stetson_grid'],
                         stet_mcc)
                plt.xlabel('stetson J stdev multiplier threshold')
                plt.ylabel('MCC')
                plt.title('MCC for stetson J')
            else:
                plt.text(0.5,0.5,
                         'stet MCC values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,2)
            if np.any(np.isfinite(stet_precision)):
                plt.plot(gridresults['stetson_grid'],
                         stet_precision)
                plt.xlabel('stetson J stdev multiplier threshold')
                plt.ylabel('precision')
                plt.title('precision for stetson J')
            else:
                plt.text(0.5,0.5,
                         'stet precision values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,3)
            if np.any(np.isfinite(stet_recall)):
                plt.plot(gridresults['stetson_grid'],
                         stet_recall)
                plt.xlabel('stetson J stdev multiplier threshold')
                plt.ylabel('recall')
                plt.title('recall for stetson J')
            else:
                plt.text(0.5,0.5,
                         'stet recall values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,4)
            if np.any(np.isfinite(stet_missed_inveta_found)):
                plt.plot(gridresults['stetson_grid'],
                         stet_missed_inveta_found)
                plt.xlabel('stetson J stdev multiplier threshold')
                plt.ylabel('# objects stetson missed but inveta found')
                plt.title('stetson J missed, inveta found')
            else:
                plt.text(0.5,0.5,
                         'stet-missed/inveta-found values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,5)
            if np.any(np.isfinite(stet_missed_iqr_found)):
                plt.plot(gridresults['stetson_grid'],
                         stet_missed_iqr_found)
                plt.xlabel('stetson J stdev multiplier threshold')
                plt.ylabel('# objects stetson missed but IQR found')
                plt.title('stetson J missed, IQR found')
            else:
                plt.text(0.5,0.5,
                         'stet-missed/IQR-found values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            # SECOND ROW: inveta plots

            plt.subplot(3,5,6)
            if np.any(np.isfinite(inveta_mcc)):
                plt.plot(gridresults['inveta_grid'],
                         inveta_mcc)
                plt.xlabel('inveta stdev multiplier threshold')
                plt.ylabel('MCC')
                plt.title('MCC for inveta')
            else:
                plt.text(0.5,0.5,
                         'inveta MCC values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,7)
            if np.any(np.isfinite(inveta_precision)):
                plt.plot(gridresults['inveta_grid'],
                         inveta_precision)
                plt.xlabel('inveta stdev multiplier threshold')
                plt.ylabel('precision')
                plt.title('precision for inveta')
            else:
                plt.text(0.5,0.5,
                         'inveta precision values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,8)
            if np.any(np.isfinite(inveta_recall)):
                plt.plot(gridresults['inveta_grid'],
                         inveta_recall)
                plt.xlabel('inveta stdev multiplier threshold')
                plt.ylabel('recall')
                plt.title('recall for inveta')
            else:
                plt.text(0.5,0.5,
                         'inveta recall values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,9)
            if np.any(np.isfinite(inveta_missed_stet_found)):
                plt.plot(gridresults['inveta_grid'],
                         inveta_missed_stet_found)
                plt.xlabel('inveta stdev multiplier threshold')
                plt.ylabel('# objects inveta missed but stetson found')
                plt.title('inveta missed, stetson J found')
            else:
                plt.text(0.5,0.5,
                         'inveta-missed-stet-found values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,10)
            if np.any(np.isfinite(inveta_missed_iqr_found)):
                plt.plot(gridresults['inveta_grid'],
                         inveta_missed_iqr_found)
                plt.xlabel('inveta stdev multiplier threshold')
                plt.ylabel('# objects inveta missed but IQR found')
                plt.title('inveta missed, IQR found')
            else:
                plt.text(0.5,0.5,
                         'inveta-missed-iqr-found values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])


            # THIRD ROW: inveta plots

            plt.subplot(3,5,11)
            if np.any(np.isfinite(iqr_mcc)):
                plt.plot(gridresults['iqr_grid'],
                         iqr_mcc)
                plt.xlabel('IQR stdev multiplier threshold')
                plt.ylabel('MCC')
                plt.title('MCC for IQR')
            else:
                plt.text(0.5,0.5,
                         'IQR MCC values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,12)
            if np.any(np.isfinite(iqr_precision)):
                plt.plot(gridresults['iqr_grid'],
                         iqr_precision)
                plt.xlabel('IQR stdev multiplier threshold')
                plt.ylabel('precision')
                plt.title('precision for IQR')
            else:
                plt.text(0.5,0.5,
                         'IQR precision values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,13)
            if np.any(np.isfinite(iqr_recall)):
                plt.plot(gridresults['iqr_grid'],
                         iqr_recall)
                plt.xlabel('IQR stdev multiplier threshold')
                plt.ylabel('recall')
                plt.title('recall for IQR')
            else:
                plt.text(0.5,0.5,
                         'IQR recall values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,14)
            if np.any(np.isfinite(iqr_missed_stet_found)):
                plt.plot(gridresults['iqr_grid'],
                         iqr_missed_stet_found)
                plt.xlabel('IQR stdev multiplier threshold')
                plt.ylabel('# objects IQR missed but stetson found')
                plt.title('IQR missed, stetson J found')
            else:
                plt.text(0.5,0.5,
                         'iqr-missed-stet-found values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])

            plt.subplot(3,5,15)
            if np.any(np.isfinite(iqr_missed_inveta_found)):
                plt.plot(gridresults['iqr_grid'],
                         iqr_missed_inveta_found)
                plt.xlabel('IQR stdev multiplier threshold')
                plt.ylabel('# objects IQR missed but inveta found')
                plt.title('IQR missed, inveta found')
            else:
                plt.text(0.5,0.5,
                         'iqr-missed-inveta-found values are all nan '
                         'for this magbin',
                         transform=plt.gca().transAxes,
                         horizontalalignment='center',
                         verticalalignment='center')
                plt.xticks([])
                plt.yticks([])


            plt.subplots_adjust(hspace=0.25,wspace=0.25)

            plt.suptitle('magcol: %s, magbin: %.3f' % (magcol, magbinmedian))

            plotdir = os.path.join(gridresults['simbasedir'],
                                   'varindex-gridsearch-plots')
            if not os.path.exists(plotdir):
                os.mkdir(plotdir)

            gridplotf = os.path.join(
                plotdir,
                '%s-magbin-%.3f-var-recoverygrid-permagbin.png' %
                (magcol, magbinmedian)
            )

            plt.savefig(gridplotf,dpi=100,bbox_inches='tight')
            plt.close('all')


            # get the best values of MCC, recall, precision and their associated
            # stet, inveta
            stet_mcc_maxind = np.where(stet_mcc == np.max(stet_mcc))
            stet_precision_maxind = np.where(
                stet_precision == np.max(stet_precision)
            )
            stet_recall_maxind = np.where(stet_recall == np.max(stet_recall))

            best_stet_mcc = stet_mcc[stet_mcc_maxind]
            best_stet_precision = stet_mcc[stet_precision_maxind]
            best_stet_recall = stet_mcc[stet_recall_maxind]

            stet_with_best_mcc = gridresults['stetson_grid'][stet_mcc_maxind]
            stet_with_best_precision = gridresults['stetson_grid'][
                stet_precision_maxind
            ]
            stet_with_best_recall = (
                gridresults['stetson_grid'][stet_recall_maxind]
            )


            inveta_mcc_maxind = np.where(inveta_mcc == np.max(inveta_mcc))
            inveta_precision_maxind = np.where(
                inveta_precision == np.max(inveta_precision)
            )
            inveta_recall_maxind = (
                np.where(inveta_recall == np.max(inveta_recall))
            )

            best_inveta_mcc = inveta_mcc[inveta_mcc_maxind]
            best_inveta_precision = inveta_mcc[inveta_precision_maxind]
            best_inveta_recall = inveta_mcc[inveta_recall_maxind]

            inveta_with_best_mcc = gridresults['inveta_grid'][inveta_mcc_maxind]
            inveta_with_best_precision = gridresults['inveta_grid'][
                inveta_precision_maxind
            ]
            inveta_with_best_recall = gridresults['inveta_grid'][
                inveta_recall_maxind
            ]


            iqr_mcc_maxind = np.where(iqr_mcc == np.max(iqr_mcc))
            iqr_precision_maxind = np.where(
                iqr_precision == np.max(iqr_precision)
            )
            iqr_recall_maxind = (
                np.where(iqr_recall == np.max(iqr_recall))
            )

            best_iqr_mcc = iqr_mcc[iqr_mcc_maxind]
            best_iqr_precision = iqr_mcc[iqr_precision_maxind]
            best_iqr_recall = iqr_mcc[iqr_recall_maxind]

            iqr_with_best_mcc = gridresults['iqr_grid'][iqr_mcc_maxind]
            iqr_with_best_precision = gridresults['iqr_grid'][
                iqr_precision_maxind
            ]
            iqr_with_best_recall = gridresults['iqr_grid'][
                iqr_recall_maxind
            ]


            plotres[magcol][magbinmedian] = {
                # stetson
                'stet_grid':gridresults['stetson_grid'],
                'stet_mcc':stet_mcc,
                'stet_precision':stet_precision,
                'stet_recall':stet_recall,
                'stet_missed_inveta_found':stet_missed_inveta_found,
                'best_stet_mcc':best_stet_mcc,
                'stet_with_best_mcc':stet_with_best_mcc,
                'best_stet_precision':best_stet_precision,
                'stet_with_best_precision':stet_with_best_precision,
                'best_stet_recall':best_stet_recall,
                'stet_with_best_recall':stet_with_best_recall,
                # inveta
                'inveta_grid':gridresults['inveta_grid'],
                'inveta_mcc':inveta_mcc,
                'inveta_precision':inveta_precision,
                'inveta_recall':inveta_recall,
                'inveta_missed_stet_found':inveta_missed_stet_found,
                'best_inveta_mcc':best_inveta_mcc,
                'inveta_with_best_mcc':inveta_with_best_mcc,
                'best_inveta_precision':best_inveta_precision,
                'inveta_with_best_precision':inveta_with_best_precision,
                'best_inveta_recall':best_inveta_recall,
                'inveta_with_best_recall':inveta_with_best_recall,
                # iqr
                'iqr_grid':gridresults['iqr_grid'],
                'iqr_mcc':iqr_mcc,
                'iqr_precision':iqr_precision,
                'iqr_recall':iqr_recall,
                'iqr_missed_stet_found':iqr_missed_stet_found,
                'best_iqr_mcc':best_iqr_mcc,
                'iqr_with_best_mcc':iqr_with_best_mcc,
                'best_iqr_precision':best_iqr_precision,
                'iqr_with_best_precision':iqr_with_best_precision,
                'best_iqr_recall':best_iqr_recall,
                'iqr_with_best_recall':iqr_with_best_recall,
                # plot info
                'recoveryplot':gridplotf
            }

            # recommend inveta, stetson index, and iqr for this magbin

            # if there are multiple stets, choose the smallest one
            if stet_with_best_mcc.size > 1:
                plotres[magcol]['best_stetsonj'].append(stet_with_best_mcc[0])
            elif stet_with_best_mcc.size > 0:
                plotres[magcol]['best_stetsonj'].append(stet_with_best_mcc[0])
            else:
                plotres[magcol]['best_stetsonj'].append(np.nan)

            # if there are multiple best invetas, choose the smallest one
            if inveta_with_best_mcc.size > 1:
                plotres[magcol]['best_inveta'].append(inveta_with_best_mcc[0])
            elif inveta_with_best_mcc.size > 0:
                plotres[magcol]['best_inveta'].append(inveta_with_best_mcc[0])
            else:
                plotres[magcol]['best_inveta'].append(np.nan)

            # if there are multiple best iqrs, choose the smallest one
            if iqr_with_best_mcc.size > 1:
                plotres[magcol]['best_iqr'].append(iqr_with_best_mcc[0])
            elif iqr_with_best_mcc.size > 0:
                plotres[magcol]['best_iqr'].append(iqr_with_best_mcc[0])
            else:
                plotres[magcol]['best_iqr'].append(np.nan)


    # write the plotresults to a pickle
    plotrespicklef = os.path.join(simbasedir,
                                  'varindex-gridsearch-magbin-results.pkl')
    with open(plotrespicklef, 'wb') as outfd:
        pickle.dump(plotres, outfd, pickle.HIGHEST_PROTOCOL)


    # recommend the values of stetson J and inveta to use
    for magcol in gridresults['magcols']:

        LOGINFO('best stdev multipliers for each %s magbin:' % magcol)
        LOGINFO('magbin    inveta    stetson J    IQR')

        for magbin, inveta, stet, iqr in zip(
                plotres[magcol]['magbinmedians'],
                plotres[magcol]['best_inveta'],
                plotres[magcol]['best_stetsonj'],
                plotres[magcol]['best_iqr']):
            LOGINFO('%.3f    %.3f    %.3f    %.3f' % (magbin,
                                                      inveta,
                                                      stet,
                                                      iqr))


    return plotres