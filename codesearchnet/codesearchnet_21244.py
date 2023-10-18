def _filter_cluster_data(self):
        """
        Filter the cluster data catalog into the filtered_data
        catalog, which is what is shown in the H-R diagram.

        Filter on the values of the sliders, as well as the lasso
        selection in the skyviewer.
        """
        min_temp = self.temperature_range_slider.value[0]
        max_temp = self.temperature_range_slider.value[1]
        temp_mask = np.logical_and(
            self.cluster.catalog['temperature'] >= min_temp,
            self.cluster.catalog['temperature'] <= max_temp
        )

        min_lum = self.luminosity_range_slider.value[0]
        max_lum = self.luminosity_range_slider.value[1]
        lum_mask = np.logical_and(
            self.cluster.catalog['luminosity'] >= min_lum,
            self.cluster.catalog['luminosity'] <= max_lum
        )

        selected_mask = np.isin(self.cluster.catalog['id'], self.selection_ids)

        filter_mask = temp_mask & lum_mask & selected_mask
        self.filtered_data = self.cluster.catalog[filter_mask].data

        self.source.data = {
            'id': list(self.filtered_data['id']),
            'temperature': list(self.filtered_data['temperature']),
            'luminosity': list(self.filtered_data['luminosity']),
            'color': list(self.filtered_data['color'])
        }

        logging.debug("Selected data is now: %s", self.filtered_data)