def register_json(self, data):
        """
        Register the contents as JSON
        """
        j = json.loads(data)
        self.last_data_timestamp = \
                datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        try:
            for v in j:
                # prepare the sensor entry container
                self.data[v[self.id_key]] = {}
                # add the mandatory entries
                self.data[v[self.id_key]][self.id_key] = \
                                            v[self.id_key]
                self.data[v[self.id_key]][self.value_key] = \
                                            v[self.value_key]
                # add the optional well known entries if provided
                if self.unit_key in v:
                    self.data[v[self.id_key]][self.unit_key] = \
                                            v[self.unit_key]
                if self.threshold_key in v:
                    self.data[v[self.id_key]][self.threshold_key] = \
                                            v[self.threshold_key]
                # add any further entries found
                for k in self.other_keys:
                    if k in v:
                        self.data[v[self.id_key]][k] = v[k]
                # add the custom sensor time
                if self.sensor_time_key in v:
                    self.data[v[self.sensor_time_key]][self.sensor_time_key] = \
                                            v[self.sensor_time_key]
                # last: add the time the data was received (overwriting any
                # not properly defined timestamp that was already there)
                self.data[v[self.id_key]][self.time_key] = \
                                            self.last_data_timestamp
        except KeyError as e:
            print("The main key was not found on the serial input line: " + \
                    str(e))
        except ValueError as e:
            print("No valid JSON string received. Waiting for the next turn.")
            print("The error was: " + str(e))