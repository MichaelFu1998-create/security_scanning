def create_risk_tear_sheet(positions,
                           style_factor_panel=None,
                           sectors=None,
                           caps=None,
                           shares_held=None,
                           volumes=None,
                           percentile=None,
                           returns=None,
                           transactions=None,
                           estimate_intraday='infer',
                           return_fig=False):
    '''
    Creates risk tear sheet: computes and plots style factor exposures, sector
    exposures, market cap exposures and volume exposures.

    Parameters
    ----------
    positions : pd.DataFrame
        Daily equity positions of algorithm, in dollars.
        - DataFrame with dates as index, equities as columns
        - Last column is cash held
        - Example:
                     Equity(24   Equity(62
                       [AAPL])      [ABT])             cash
        2017-04-03	-108062.40 	  4401.540     2.247757e+07
        2017-04-04	-108852.00	  4373.820     2.540999e+07
        2017-04-05	-119968.66	  4336.200     2.839812e+07

    style_factor_panel : pd.Panel
        Panel where each item is a DataFrame that tabulates style factor per
        equity per day.
        - Each item has dates as index, equities as columns
        - Example item:
                     Equity(24   Equity(62
                       [AAPL])      [ABT])
        2017-04-03	  -0.51284     1.39173
        2017-04-04	  -0.73381     0.98149
        2017-04-05	  -0.90132	   1.13981

    sectors : pd.DataFrame
        Daily Morningstar sector code per asset
        - DataFrame with dates as index and equities as columns
        - Example:
                     Equity(24   Equity(62
                       [AAPL])      [ABT])
        2017-04-03	     311.0       206.0
        2017-04-04	     311.0       206.0
        2017-04-05	     311.0	     206.0

    caps : pd.DataFrame
        Daily market cap per asset
        - DataFrame with dates as index and equities as columns
        - Example:
                          Equity(24        Equity(62
                            [AAPL])           [ABT])
        2017-04-03     1.327160e+10     6.402460e+10
        2017-04-04	   1.329620e+10     6.403694e+10
        2017-04-05	   1.297464e+10	    6.397187e+10

    shares_held : pd.DataFrame
        Daily number of shares held by an algorithm.
        - Example:
                          Equity(24        Equity(62
                            [AAPL])           [ABT])
        2017-04-03             1915            -2595
        2017-04-04	           1968            -3272
        2017-04-05	           2104            -3917

    volumes : pd.DataFrame
        Daily volume per asset
        - DataFrame with dates as index and equities as columns
        - Example:
                          Equity(24        Equity(62
                            [AAPL])           [ABT])
        2017-04-03      34940859.00       4665573.80
        2017-04-04	    35603329.10       4818463.90
        2017-04-05	    41846731.75	      4129153.10

    percentile : float
        Percentile to use when computing and plotting volume exposures.
        - Defaults to 10th percentile
    '''

    positions = utils.check_intraday(estimate_intraday, returns,
                                     positions, transactions)

    idx = positions.index & style_factor_panel.iloc[0].index & sectors.index \
        & caps.index & shares_held.index & volumes.index
    positions = positions.loc[idx]

    vertical_sections = 0
    if style_factor_panel is not None:
        vertical_sections += len(style_factor_panel.items)
        new_style_dict = {}
        for item in style_factor_panel.items:
            new_style_dict.update({item:
                                   style_factor_panel.loc[item].loc[idx]})
        style_factor_panel = pd.Panel()
        style_factor_panel = style_factor_panel.from_dict(new_style_dict)
    if sectors is not None:
        vertical_sections += 4
        sectors = sectors.loc[idx]
    if caps is not None:
        vertical_sections += 4
        caps = caps.loc[idx]
    if (shares_held is not None) & (volumes is not None) \
                                 & (percentile is not None):
        vertical_sections += 3
        shares_held = shares_held.loc[idx]
        volumes = volumes.loc[idx]

    if percentile is None:
        percentile = 0.1

    fig = plt.figure(figsize=[14, vertical_sections * 6])
    gs = gridspec.GridSpec(vertical_sections, 3, wspace=0.5, hspace=0.5)

    if style_factor_panel is not None:
        style_axes = []
        style_axes.append(plt.subplot(gs[0, :]))
        for i in range(1, len(style_factor_panel.items)):
            style_axes.append(plt.subplot(gs[i, :], sharex=style_axes[0]))

        j = 0
        for name, df in style_factor_panel.iteritems():
            sfe = risk.compute_style_factor_exposures(positions, df)
            risk.plot_style_factor_exposures(sfe, name, style_axes[j])
            j += 1

    if sectors is not None:
        i += 1
        ax_sector_longshort = plt.subplot(gs[i:i+2, :], sharex=style_axes[0])
        i += 2
        ax_sector_gross = plt.subplot(gs[i, :], sharex=style_axes[0])
        i += 1
        ax_sector_net = plt.subplot(gs[i, :], sharex=style_axes[0])
        long_exposures, short_exposures, gross_exposures, net_exposures \
            = risk.compute_sector_exposures(positions, sectors)
        risk.plot_sector_exposures_longshort(long_exposures, short_exposures,
                                             ax=ax_sector_longshort)
        risk.plot_sector_exposures_gross(gross_exposures, ax=ax_sector_gross)
        risk.plot_sector_exposures_net(net_exposures, ax=ax_sector_net)

    if caps is not None:
        i += 1
        ax_cap_longshort = plt.subplot(gs[i:i+2, :], sharex=style_axes[0])
        i += 2
        ax_cap_gross = plt.subplot(gs[i, :], sharex=style_axes[0])
        i += 1
        ax_cap_net = plt.subplot(gs[i, :], sharex=style_axes[0])
        long_exposures, short_exposures, gross_exposures, net_exposures \
            = risk.compute_cap_exposures(positions, caps)
        risk.plot_cap_exposures_longshort(long_exposures, short_exposures,
                                          ax_cap_longshort)
        risk.plot_cap_exposures_gross(gross_exposures, ax_cap_gross)
        risk.plot_cap_exposures_net(net_exposures, ax_cap_net)

    if volumes is not None:
        i += 1
        ax_vol_longshort = plt.subplot(gs[i:i+2, :], sharex=style_axes[0])
        i += 2
        ax_vol_gross = plt.subplot(gs[i, :], sharex=style_axes[0])
        longed_threshold, shorted_threshold, grossed_threshold \
            = risk.compute_volume_exposures(positions, volumes, percentile)
        risk.plot_volume_exposures_longshort(longed_threshold,
                                             shorted_threshold, percentile,
                                             ax_vol_longshort)
        risk.plot_volume_exposures_gross(grossed_threshold, percentile,
                                         ax_vol_gross)

    for ax in fig.axes:
        plt.setp(ax.get_xticklabels(), visible=True)

    if return_fig:
        return fig