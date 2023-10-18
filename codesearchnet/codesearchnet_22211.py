def get_shifts(self, params={}):
        """
        List shifts

        http://dev.wheniwork.com/#listing-shifts
        """
        param_list = [(k, params[k]) for k in sorted(params)]
        url = "/2/shifts/?%s" % urlencode(param_list)

        data = self._get_resource(url)
        shifts = []
        locations = {}
        sites = {}
        positions = {}
        users = {}
        for entry in data.get("locations", []):
            location = Locations.location_from_json(entry)
            locations[location.location_id] = location
        for entry in data.get("sites", []):
            site = Sites.site_from_json(entry)
            sites[site.site_id] = site
        for entry in data.get("positions", []):
            position = Positions.position_from_json(entry)
            positions[position.position_id] = position
        for entry in data.get("users", []):
            user = Users.user_from_json(entry)
            users[user.user_id] = user
        for entry in data["shifts"]:
            shift = self.shift_from_json(entry)
            shifts.append(shift)

        for shift in shifts:
            shift.location = locations.get(shift.location_id, None)
            shift.site = sites.get(shift.site_id, None)
            shift.position = positions.get(shift.position_id, None)
            shift.user = users.get(shift.user_id, None)

        return shifts