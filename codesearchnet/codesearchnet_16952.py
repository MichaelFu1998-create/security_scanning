def get_md_device(self, line, personalities=[]):
        """Return a dict of md device define in the line."""
        ret = {}

        splitted = split('\W+', line)
        # Raid status
        # Active or 'started'. An inactive array is usually faulty.
        # Stopped arrays aren't visible here.
        ret['status'] = splitted[1]
        if splitted[2] in personalities:
            # Raid type (ex: RAID5)
            ret['type'] = splitted[2]
            # Array's components
            ret['components'] = self.get_components(line, with_type=True)
        else:
            # Raid type (ex: RAID5)
            ret['type'] = None
            # Array's components
            ret['components'] = self.get_components(line, with_type=False)

        return ret