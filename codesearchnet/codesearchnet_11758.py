def get_combined_requirements(self, requirements=None):
        """
        Returns all requirements files combined into one string.
        """

        requirements = requirements or self.env.requirements

        def iter_lines(fn):
            with open(fn, 'r') as fin:
                for line in fin.readlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    yield line

        content = []
        if isinstance(requirements, (tuple, list)):
            for f in requirements:
                f = self.find_template(f)
                content.extend(list(iter_lines(f)))
        else:
            assert isinstance(requirements, six.string_types)
            f = self.find_template(requirements)
            content.extend(list(iter_lines(f)))

        return '\n'.join(content)