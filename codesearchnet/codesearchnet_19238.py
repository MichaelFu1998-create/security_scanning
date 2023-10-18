def main_cli():
    """
     Actualiza la base de datos de PVPC/DEMANDA almacenados como dataframe en local,
     creando una nueva si no existe o hubiere algún problema. Los datos registrados se guardan en HDF5
    """

    def _get_parser_args():
        p = argparse.ArgumentParser(description='Gestor de DB de PVPC/DEMANDA (esios.ree.es)')
        p.add_argument('-d', '--dem', action='store_true', help='Selecciona BD de demanda (BD de PVPC por defecto)')
        p.add_argument('-i', '--info', action='store', nargs='*',
                       help="Muestra información de la BD seleccionada.      "
                            "* Puede usar intervalos temporales y nombres de columnas, "
                            "como '-i gen noc 2017-01-24 2017-01-26'")
        p.add_argument('-fu', '-FU', '--forceupdate', action='store_true',
                       help="Fuerza la reconstrucción total de la BD seleccionada")
        p.add_argument('-u', '-U', '--update', action='store_true',
                       help="Actualiza la información de la BD seleccionada hasta el instante actual")
        p.add_argument('-p', '--plot', action='store_true', help="Genera plots de la información filtrada de la BD")
        p.add_argument('-v', '--verbose', action='store_true', help='Muestra información extra')
        arguments = p.parse_args()
        return arguments, p

    def _parse_date(string, columns):
        try:
            ts = pd.Timestamp(string)
            print_cyan('{} es timestamp: {:%c} --> {}'.format(string, ts, ts.date()))
            columns.remove(string)
            return ts.date().isoformat()
        except ValueError:
            pass

    args, parser = _get_parser_args()
    print_secc('ESIOS PVPC/DEMANDA')
    if args.dem:
        db_web = DatosREE(update=args.update, force_update=args.forceupdate, verbose=args.verbose)
    else:
        db_web = PVPC(update=args.update, force_update=args.forceupdate, verbose=args.verbose)
    data = db_web.data['data']
    if args.info is not None:
        if len(args.info) > 0:
            cols = args.info.copy()
            dates = [d for d in [_parse_date(s, cols) for s in args.info] if d]
            if len(dates) == 2:
                data = data.loc[dates[0]:dates[1]]
            elif len(dates) == 1:
                data = data.loc[dates[0]]
            if len(cols) > 0:
                try:
                    data = data[[c.upper() for c in cols]]
                except KeyError as e:
                    print_red('NO SE PUEDE FILTRAR LA COLUMNA (Exception: {})\nLAS COLUMNAS DISPONIBLES SON:\n{}'
                              .format(e, data.columns))
            print_info(data)
        else:
            print_secc('LAST 24h in DB:')
            print_info(data.iloc[-24:])
            print_cyan(data.columns)
    if args.plot:
        if args.dem:
            from esiosdata.pvpcplot import pvpcplot_tarifas_hora, pvpcplot_grid_hora
            print_red('IMPLEMENTAR PLOTS DEM')
        else:
            from esiosdata.pvpcplot import pvpcplot_tarifas_hora, pvpcplot_grid_hora
            if len(data) < 750:
                pvpcplot_grid_hora(data)
                # pvpcplot_tarifas_hora(data)
            else:
                print_red('La selección para plot es excesiva: {} samples de {} a {}\nSe hace plot de las últimas 24h'.
                          format(len(data), data.index[0], data.index[-1]))
                pvpcplot_grid_hora(db_web.data['data'].iloc[-24:])
                pvpcplot_tarifas_hora(db_web.data['data'].iloc[-24:])