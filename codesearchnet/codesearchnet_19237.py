def get_data_perfiles_estimados_2017(force_download=False):
    """Extrae perfiles estimados para 2017 con el formato de los CSV's mensuales con los perfiles definitivos.
    :param force_download: bool para forzar la descarga del excel de la web de REE.
    :return: perfiles_2017
    :rtype: pd.Dataframe
    """
    global DATA_PERFILES_2017
    if (DATA_PERFILES_2017 is None) or force_download:
        perf_demref_2017, _ = get_data_coeficientes_perfilado_2017(force_download=force_download)
        # Conversión de formato de dataframe de perfiles 2017 a finales (para uniformizar):
        cols_usar = ['Pa,0m,d,h', 'Pb,0m,d,h', 'Pc,0m,d,h', 'Pd,0m,d,h']
        perfs_2017 = perf_demref_2017[cols_usar].copy()
        perfs_2017.columns = ['COEF. PERFIL {}'.format(p) for p in 'ABCD']
        DATA_PERFILES_2017 = perfs_2017
        return perfs_2017
    return DATA_PERFILES_2017