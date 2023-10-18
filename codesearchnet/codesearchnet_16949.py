def load(self):
        """Return a dict of stats."""
        ret = {}

        # Read the mdstat file
        with open(self.get_path(), 'r') as f:
            # lines is a list of line (with \n)
            lines = f.readlines()

        # First line: get the personalities
        # The "Personalities" line tells you what RAID level the kernel currently supports.
        # This can be changed by either changing the raid modules or recompiling the kernel.
        # Possible personalities include: [raid0] [raid1] [raid4] [raid5] [raid6] [linear] [multipath] [faulty]
        ret['personalities'] = self.get_personalities(lines[0])

        # Second to last before line: Array definition
        ret['arrays'] = self.get_arrays(lines[1:-1], ret['personalities'])

        # Save the file content as it for the __str__ method
        self.content = reduce(lambda x, y: x + y, lines)

        return ret