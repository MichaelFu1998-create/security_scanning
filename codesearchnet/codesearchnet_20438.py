def parse(cls, path):
        """Parses out parameters and separates them out of the path.

        This uses one of the many defined patterns on the options class. But,
        it defaults to a no-op if there are no defined patterns.
        """
        # Iterate through the available patterns.
        for resource, pattern in cls.meta.patterns:
            # Attempt to match the path.
            match = re.match(pattern, path)
            if match is not None:
                # Found something.
                return resource, match.groupdict(), match.string[match.end():]

        # No patterns at all; return unsuccessful.
        return None if not cls.meta.patterns else False