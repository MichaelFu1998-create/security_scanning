def pvpc_calc_tcu_cp_feu_d(df, verbose=True, convert_kwh=True):
    """Procesa TCU, CP, FEU diario.

    :param df:
    :param verbose:
    :param convert_kwh:
    :return:
    """
    if 'TCU' + TARIFAS[0] not in df.columns:
        # Pasa de €/MWh a €/kWh:
        if convert_kwh:
            cols_mwh = [c + t for c in COLS_PVPC for t in TARIFAS if c != 'COF']
            df[cols_mwh] = df[cols_mwh].applymap(lambda x: x / 1000.)
        # Obtiene columnas TCU, CP, precio día
        gb_t = df.groupby(lambda x: TARIFAS[np.argmax([t in x for t in TARIFAS])], axis=1)
        for k, g in gb_t:
            if verbose:
                print('TARIFA {}'.format(k))
                print(g.head())

            # Cálculo de TCU
            df['TCU{}'.format(k)] = g[k] - g['TEU{}'.format(k)]

            # Cálculo de CP
            # cols_cp = [c + k for c in ['FOS', 'FOM', 'INT', 'PCAP', 'PMH', 'SAH']]
            cols_cp = [c + k for c in COLS_PVPC if c not in ['', 'COF', 'TEU']]
            df['CP{}'.format(k)] = g[cols_cp].sum(axis=1)

            # Cálculo de PERD --> No es posible así, ya que los valores base ya vienen con PERD
            # dfs_pvpc[k]['PERD{}'.format(k)] = dfs_pvpc[k]['TCU{}'.format(k)] / dfs_pvpc[k]['CP{}'.format(k)]
            # dfs_pvpc[k]['PERD{}'.format(k)] = dfs_pvpc[k]['INT{}'.format(k)] / 1.92

            # Cálculo de FEU diario
            cols_k = ['TEU' + k, 'TCU' + k, 'COF' + k]
            g = df[cols_k].groupby('TEU' + k)
            pr = g.apply(lambda x: x['TCU' + k].dot(x['COF' + k]) / x['COF' + k].sum())
            pr.name = 'PD_' + k
            df = df.join(pr, on='TEU' + k, rsuffix='_r')
            df['PD_' + k] += df['TEU' + k]
    return df