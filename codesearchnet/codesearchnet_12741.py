def _determine_supported_alleles(command, supported_allele_flag):
        """
        Try asking the commandline predictor (e.g. netMHCpan)
        which alleles it supports.
        """
        try:
            # convert to str since Python3 returns a `bytes` object
            supported_alleles_output = check_output([
                command, supported_allele_flag
            ])
            supported_alleles_str = supported_alleles_output.decode("ascii", "ignore")
            assert len(supported_alleles_str) > 0, \
                '%s returned empty allele list' % command
            supported_alleles = set([])
            for line in supported_alleles_str.split("\n"):
                line = line.strip()
                if not line.startswith('#') and len(line) > 0:
                    try:
                        # We need to normalize these alleles (the output of the predictor
                        # when it lists its supported alleles) so that they are comparable with
                        # our own alleles.
                        supported_alleles.add(normalize_allele_name(line))
                    except AlleleParseError as error:
                        logger.info("Skipping allele %s: %s", line, error)
                        continue
            if len(supported_alleles) == 0:
                raise ValueError("Unable to determine supported alleles")
            return supported_alleles
        except Exception as e:
            logger.exception(e)
            raise SystemError("Failed to run %s %s. Possibly an incorrect executable version?" % (
                command,
                supported_allele_flag))