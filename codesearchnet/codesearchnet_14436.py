def _get_param_names(self):
        """
        Get mappable parameters from YAML.
        """
        template = Template(self.yaml_string)
        names = ['yaml_string']  # always include the template
        for match in re.finditer(template.pattern, template.template):
            name = match.group('named') or match.group('braced')
            assert name is not None
            names.append(name)
        return names