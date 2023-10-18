def procesa_data_dia(self, key_dia, datos_para_procesar):
        """Procesa los datos descargados correspondientes a un día `key_dia`."""
        return pvpc_procesa_datos_dia(key_dia, datos_para_procesar, verbose=self.verbose)