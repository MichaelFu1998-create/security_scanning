def integridad_data(self, data_integr=None, key=None):
        """
        Definici�n espec�fica para comprobar timezone y frecuencia de los datos, adem�s de comprobar
        que el index de cada dataframe de la base de datos sea de fechas, �nico (sin duplicados) y creciente
        :param data_integr:
        :param key:
        """
        if data_integr is None and key is None and all(k in self.data.keys() for k in KEYS_DATA_DEM):
            assert(self.data[KEYS_DATA_DEM[0]].index.freq == FREQ_DAT_DEM
                   and self.data[KEYS_DATA_DEM[0]].index.tz == self.TZ)
            if self.data[KEYS_DATA_DEM[1]] is not None:
                assert(self.data[KEYS_DATA_DEM[1]].index.freq == 'D')
        super(DatosREE, self).integridad_data(data_integr, key)