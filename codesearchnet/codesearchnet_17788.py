def validate_bands(self, bands):
        """Validate bands parameter."""
        if not isinstance(bands, list):
            logger.error('Parameter bands must be a "list"')
            raise TypeError('Parameter bands must be a "list"')
        valid_bands = list(range(1, 12)) + ['BQA']
        for band in bands:
            if band not in valid_bands:
                logger.error('%s is not a valid band' % band)
                raise InvalidBandError('%s is not a valid band' % band)