def predict(self, sequences):
        """
        Return netChop predictions for each position in each sequence.

        Parameters
        -----------
        sequences : list of string
            Amino acid sequences to predict cleavage for

        Returns
        -----------
        list of list of float

        The i'th list corresponds to the i'th sequence. Each list gives
        the cleavage probability for each position in the sequence.
        """
        with tempfile.NamedTemporaryFile(suffix=".fsa", mode="w") as input_fd:
            for (i, sequence) in enumerate(sequences):
                input_fd.write("> %d\n" % i)
                input_fd.write(sequence)
                input_fd.write("\n")
            input_fd.flush()
            try:
                output = subprocess.check_output(["netChop", input_fd.name])
            except subprocess.CalledProcessError as e:
                logging.error("Error calling netChop: %s:\n%s" % (e, e.output))
                raise

        parsed = self.parse_netchop(output)
        assert len(parsed) == len(sequences), \
            "Expected %d results but got %d" % (
                len(sequences), len(parsed))
        assert [len(x) for x in parsed] == [len(x) for x in sequences]
        return parsed