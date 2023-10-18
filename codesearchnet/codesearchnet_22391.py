def get_text(self):
        """
        Get the data in text form (i.e. human readable)
        """
        t = "==== " + str(self.last_data_timestamp) + " ====\n"
        for k in self.data:
            t += k + " " + str(self.data[k][self.value_key])
            u = ""
            if self.unit_key in self.data[k]:
                u = self.data[k][self.unit_key]
                t += u
            if self.threshold_key in self.data[k]:
                if (self.data[k][self.threshold_key] < \
                                    self.data[k][self.value_key]):
                    t += " !Warning: Value is over threshold: " + \
                                str(self.data[k][self.threshold_key]) + "!"
                else:
                    t += " (" + str(self.data[k][self.threshold_key]) + u + ")"
            for l in self.other_keys:
                if l in self.data[k]:
                    t += " " + self.data[k][l]
            t += "\n"
        return t