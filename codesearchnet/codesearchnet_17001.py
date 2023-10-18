def create_series(self, num_series, batch_size=5000):
        """
        Write one data point for each series name to initialize the series
        :param num_series: Number of different series names to create
        :param batch_size: Number of series to create at the same time
        :return:
        """
        datapoints = []
        for _ in range(num_series):
            name = self.dummy_seriesname()
            datapoints.append(self.create_datapoint(name, ["value"], [[1]]))
        for data in tqdm(self.batch(datapoints, batch_size)):
            self.client.write_points(data)