def get_resample_data(self):
        """Obtiene los dataframes de los datos de PVPC con resampling diario y mensual."""
        if self.data is not None:
            if self._pvpc_mean_daily is None:
                self._pvpc_mean_daily = self.data['data'].resample('D').mean()
            if self._pvpc_mean_monthly is None:
                self._pvpc_mean_monthly = self.data['data'].resample('MS').mean()
        return self._pvpc_mean_daily, self._pvpc_mean_monthly