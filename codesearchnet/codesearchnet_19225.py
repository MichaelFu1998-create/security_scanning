def dem_url_dia(dt_day='2015-06-22'):
    """Obtiene las urls de descarga de los datos de demanda energética de un día concreto."""

    def _url_tipo_dato(str_dia, k):
        url = SERVER + '/archives/{}/download_json?locale=es'.format(D_TIPOS_REQ_DEM[k])
        if type(str_dia) is str:
            return url + '&date=' + str_dia
        else:
            return url + '&date=' + str_dia.date().isoformat()

    urls = [_url_tipo_dato(dt_day, k) for k in D_TIPOS_REQ_DEM.keys()]
    return urls