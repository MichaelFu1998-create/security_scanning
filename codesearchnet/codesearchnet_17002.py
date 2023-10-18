def write_points(self, series_name, start_date, end_date, resolution=10, batch_size=5000):
        """
        Create sample datapoints between two dates with the given resolution (in seconds)
        :param series_name:
        :param start_date:
        :param end_date:
        :param resolution:
        :param batch_size:
        """
        start_ts = int(start_date.strftime("%s"))
        end_ts = int(end_date.strftime("%s"))

        range_seconds = end_ts - start_ts
        num_datapoints = range_seconds / resolution

        timestamps = [start_ts + i * resolution for i in range(num_datapoints)]

        columns = ["time", "value"]
        for batch in tqdm(self.batch(timestamps, batch_size)):
            points = []
            for timestamp in batch:
                point = random.randint(1, 100)
                points.append([timestamp, point])
            datapoint = self.create_datapoint(series_name, columns, points)
            self.client.write_points([datapoint])