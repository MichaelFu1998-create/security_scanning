def last_entry(self, data_revisar=None, key_revisar=None):
        """
        Definición específica para filtrar por datos de demanda energética (pues los datos se extienden más allá del
        tiempo presente debido a las columnas de potencia prevista y programada.

        :param data_revisar: (OPC) Se puede pasar un dataframe específico
        :param key_revisar: (OPC) Normalmente, para utilizar 'dem'
        :return: tmax, num_entradas
        """
        if data_revisar is None and key_revisar is None:
            data_revisar = self.data[self.masterkey][pd.notnull(self.data[self.masterkey]['dem'])]
            super(DatosREE, self).printif('Últimos valores de generación y demanda:', 'info')
            super(DatosREE, self).printif(data_revisar.tail(), 'info')
            return super(DatosREE, self).last_entry(data_revisar, 'dem')
        else:
            return super(DatosREE, self).last_entry(data_revisar, key_revisar)