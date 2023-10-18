def example(self, relative_path):
        """Load an example from the knitting pattern examples.

        :param str relative_path: the path to load
        :return: the result of the processing

        You can use :meth:`knittingpattern.Loader.PathLoader.examples`
        to find out the paths of all examples.
        """
        example_path = os.path.join("examples", relative_path)
        return self.relative_file(__file__, example_path)