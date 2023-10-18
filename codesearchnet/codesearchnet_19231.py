def pvpc_url_dia(dt_day):
    """Obtiene la url de descarga de los datos de PVPC de un día concreto.

    Anteriormente era: 'http://www.esios.ree.es/Solicitar?fileName=pvpcdesglosehorario_' + str_dia
    + '&fileType=xml&idioma=es', pero ahora es en JSON y requiere token_auth en headers.
    """
    if type(dt_day) is str:
        return SERVER + '/archives/70/download_json?locale=es' + '&date=' + dt_day
    else:
        return SERVER + '/archives/70/download_json?locale=es' + '&date=' + dt_day.date().isoformat()