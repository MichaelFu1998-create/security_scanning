def busca_errores_data(self):
        """
        Busca errores o inconsistencias en los datos adquiridos
        :return: Dataframe de errores encontrados
        """
        data_busqueda = self.append_delta_index(TS_DATA_DEM, data_delta=self.data[self.masterkey].copy())
        idx_desconex = (((data_busqueda.index < 'now') & (data_busqueda.index >= self.DATE_INI)) &
                        ((data_busqueda.delta_T > 1) | data_busqueda['dem'].isnull() |
                         data_busqueda['pre'].isnull() | data_busqueda['pro'].isnull()))
        sosp = data_busqueda[idx_desconex].copy()
        assert len(sosp) == 0
        # if len(sosp) > 0:
        #     cols_show = ['bad_dem', 'bad_pre', 'bad_T', 'delta', 'delta_T', 'dem', 'pre', 'pro']
        #     cols_ss = cols_show[:3]
        #     how_r = {k: pd.Series.sum if k == 'delta' else 'sum' for k in cols_show}
        #     sosp[cols_show[0]] = sosp['dem'].isnull()
        #     sosp[cols_show[1]] = sosp['pre'].isnull()
        #     sosp[cols_show[2]] = sosp['delta_T'] > 1
        #     if verbose:
        #         print(sosp[cols_show].tz_localize(None).resample('D', how=how_r).dropna(how='all', subset=cols_ss))
        #         print(sosp[cols_show].tz_localize(None).resample('MS', how=how_r).dropna(how='all', subset=cols_ss))
        #     return sosp
        return pd.DataFrame()