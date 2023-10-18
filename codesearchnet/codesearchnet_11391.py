def consume(self, istream, ostream, batch=False):
        """Read points from istream and output to ostream."""
        datapoints = []  # List of 2-tuples

        if batch:
            sleep = max(0.01, self.option.sleep)
            fd = istream.fileno()
            while True:
                try:
                    if select.select([fd], [], [], sleep):
                        try:
                            line = istream.readline()
                            if line == '':
                                break
                            datapoints.append(self.consume_line(line))
                        except ValueError:
                            continue

                        if self.option.sort_by_column:
                            datapoints = sorted(datapoints, key=itemgetter(self.option.sort_by_column - 1))

                        if len(datapoints) > 1:
                            datapoints = datapoints[-self.maximum_points:]
                            self.update([dp[0] for dp in datapoints], [dp[1] for dp in datapoints])
                            self.render(ostream)

                        time.sleep(sleep)

                except KeyboardInterrupt:
                    break

        else:
            for line in istream:
                try:
                    datapoints.append(self.consume_line(line))
                except ValueError:
                    pass

            if self.option.sort_by_column:
                datapoints = sorted(datapoints, key=itemgetter(self.option.sort_by_column - 1))

            self.update([dp[0] for dp in datapoints], [dp[1] for dp in datapoints])
            self.render(ostream)