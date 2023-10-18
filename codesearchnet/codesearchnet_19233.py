def pvpc_procesa_datos_dia(_, response, verbose=True):
    """Procesa la información JSON descargada y forma el dataframe de los datos de un día."""
    try:
        d_data = response['PVPC']
        df = _process_json_pvpc_hourly_data(pd.DataFrame(d_data))
        return df, 0
    except Exception as e:
        if verbose:
            print('ERROR leyendo información de web: {}'.format(e))
        return None, -2