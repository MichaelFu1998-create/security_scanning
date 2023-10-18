def get_observations(self):
        """
        Parses the HTML table into a list of dictionaries, each of which
        represents a single observation.
        """
        if self.empty:
            return []
        rows = list(self.tbody)
        observations = []
        for row_observation, row_details in zip(rows[::2], rows[1::2]):
            data = {}
            cells = OBSERVATION_XPATH(row_observation)
            data['name'] = _clean_cell(cells[0])
            data['date'] = _clean_cell(cells[1])
            data['magnitude'] = _clean_cell(cells[3])
            data['obscode'] = _clean_cell(cells[6])
            cells = DETAILS_XPATH(row_details)
            data['comp1'] = _clean_cell(cells[0])
            data['chart'] = _clean_cell(cells[3]).replace('None', '')
            data['comment_code'] = _clean_cell(cells[4])
            data['notes'] = _clean_cell(cells[5])
            observations.append(data)
        return observations