def _check_collisions(self, new_range, existing_ranges):
        """Check for overlapping ranges."""
        def _contains(num, r1):
            return (num >= r1[0] and
                    num <= r1[1])

        def _is_overlap(r1, r2):
            return (_contains(r1[0], r2) or
                    _contains(r1[1], r2) or
                    _contains(r2[0], r1) or
                    _contains(r2[1], r1))

        for existing_range in existing_ranges:
            if _is_overlap(new_range, existing_range):
                return True
        return False