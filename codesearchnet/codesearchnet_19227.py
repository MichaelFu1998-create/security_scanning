def dem_data_dia(str_dia='2015-10-10', str_dia_fin=None):
    """Obtiene datos de demanda energética en un día concreto o un intervalo, accediendo directamente a la web."""
    params = {'date_fmt': DATE_FMT, 'usar_multithread': False, 'num_retries': 1, "timeout": 10,
              'func_procesa_data_dia': dem_procesa_datos_dia, 'func_url_data_dia': dem_url_dia,
              'data_extra_request': {'json_req': False, 'headers': HEADERS}}
    if str_dia_fin is not None:
        params['usar_multithread'] = True
        data, hay_errores, str_import = get_data_en_intervalo(str_dia, str_dia_fin, **params)
    else:
        data, hay_errores, str_import = get_data_en_intervalo(str_dia, str_dia, **params)
    if not hay_errores:
        return data
    else:
        print_err(str_import)
        return None