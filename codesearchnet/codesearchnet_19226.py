def dem_procesa_datos_dia(key_day, response):
    """Procesa los datos descargados en JSON."""
    dfs_import, df_import, dfs_maxmin, hay_errores = [], None, [], 0
    for r in response:
        tipo_datos, data = _extract_func_json_data(r)
        if tipo_datos is not None:
            if ('IND_MaxMin' in tipo_datos) and data:
                df_import = _import_daily_max_min(data)
                dfs_maxmin.append(df_import)
            elif data:
                df_import = _import_json_ts_data(data)
                dfs_import.append(df_import)
        if tipo_datos is None or df_import is None:
            hay_errores += 1
    if hay_errores == 4:
        # No hay nada, salida temprana sin retry:
        print_redb('** No hay datos para el día {}!'.format(key_day))
        return None, -2
    else:  # if hay_errores < 3:
        # TODO formar datos incompletos!! (max-min con NaN's, etc.)
        data_import = {}
        if dfs_import:
            data_import[KEYS_DATA_DEM[0]] = dfs_import[0].join(dfs_import[1])
        if len(dfs_maxmin) == 2:
            data_import[KEYS_DATA_DEM[1]] = dfs_maxmin[0].join(dfs_maxmin[1])
        elif dfs_maxmin:
            data_import[KEYS_DATA_DEM[1]] = dfs_maxmin[0]
        if not data_import:
            print_err('DÍA: {} -> # ERRORES: {}'.format(key_day, hay_errores))
            return None, -2
        return data_import, 0