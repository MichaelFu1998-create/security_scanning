def get_data_coeficientes_perfilado_2017(force_download=False):
    """Extrae la información de las dos hojas del Excel proporcionado por REE
    con los perfiles iniciales para 2017.
    :param force_download: Descarga el fichero 'raw' del servidor, en vez de acudir a la copia local.
    :return: perfiles_2017, coefs_alpha_beta_gamma
    :rtype: tuple
    """
    path_perfs = os.path.join(STORAGE_DIR, 'perfiles_consumo_2017.h5')

    if force_download or not os.path.exists(path_perfs):
        # Coeficientes de perfilado y demanda de referencia (1ª hoja)
        cols_sheet1 = ['Mes', 'Día', 'Hora',
                       'Pa,0m,d,h', 'Pb,0m,d,h', 'Pc,0m,d,h', 'Pd,0m,d,h', 'Demanda de Referencia 2017 (MW)']
        perfs_2017 = pd.read_excel(URL_PERFILES_2017, header=None, skiprows=[0, 1], names=cols_sheet1)
        perfs_2017['ts'] = pd.DatetimeIndex(start='2017-01-01', freq='H', tz=TZ, end='2017-12-31 23:59')
        perfs_2017 = perfs_2017.set_index('ts').drop(['Mes', 'Día', 'Hora'], axis=1)

        # Coefs Alfa, Beta, Gamma (2ª hoja):
        coefs_alpha_beta_gamma = pd.read_excel(URL_PERFILES_2017, sheetname=1)
        print('Escribiendo perfiles 2017 en disco, en {}'.format(path_perfs))
        with pd.HDFStore(path_perfs, 'w') as st:
            st.put('coefs', coefs_alpha_beta_gamma)
            st.put('perfiles', perfs_2017)
        print('HDFStore de tamaño {:.3f} KB'.format(os.path.getsize(path_perfs) / 1000))
    else:
        with pd.HDFStore(path_perfs, 'r') as st:
            coefs_alpha_beta_gamma = st['coefs']
            perfs_2017 = st['perfiles']
    return perfs_2017, coefs_alpha_beta_gamma