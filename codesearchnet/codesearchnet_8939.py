def json(self, validate=True, *args, **kwargs):
        """
        returns a string formatted as **NetJSON DeviceConfiguration**;
        performs validation before returning output;

        ``*args`` and ``*kwargs`` will be passed to ``json.dumps``;

        :returns: string
        """
        if validate:
            self.validate()
        # automatically adds NetJSON type
        config = deepcopy(self.config)
        config.update({'type': 'DeviceConfiguration'})
        return json.dumps(config, *args, **kwargs)