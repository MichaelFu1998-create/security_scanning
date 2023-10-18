def _most_popular_gender(self, name, counter):
        """Finds the most popular gender for the given name counting by given counter"""
        if name not in self.names:
            return self.unknown_value

        max_count, max_tie = (0, 0)
        best = self.names[name].keys()[0]
        for gender, country_values in self.names[name].items():
            count, tie = counter(country_values)
            if count > max_count or (count == max_count and tie > max_tie):
                max_count, max_tie, best = count, tie, gender

        return best if max_count > 0 else self.unknown_value