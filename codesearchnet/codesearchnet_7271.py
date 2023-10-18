def guess_format(self, field):
        """
        Returns the correct faker function based on the field type
        :param field:
        """
        faker = self.faker
        provider = self.provider

        if isinstance(field, DurationField): return lambda x: provider.duration()
        if isinstance(field, UUIDField): return lambda x: provider.uuid()

        if isinstance(field, BooleanField): return lambda x: faker.boolean()
        if isinstance(field, NullBooleanField): return lambda x: faker.null_boolean()
        if isinstance(field, PositiveSmallIntegerField): return lambda x: provider.rand_small_int(pos=True)
        if isinstance(field, SmallIntegerField): return lambda x: provider.rand_small_int()
        if isinstance(field, BigIntegerField): return lambda x: provider.rand_big_int()
        if isinstance(field, PositiveIntegerField): return lambda x: provider.rand_small_int(pos=True)
        if isinstance(field, IntegerField): return lambda x: provider.rand_small_int()
        if isinstance(field, FloatField): return lambda x: provider.rand_float()
        if isinstance(field, DecimalField): return lambda x: random.random()

        if isinstance(field, URLField): return lambda x: faker.uri()
        if isinstance(field, SlugField): return lambda x: faker.uri_page()
        if isinstance(field, IPAddressField) or isinstance(field, GenericIPAddressField):
            protocol = random.choice(['ipv4','ipv6'])
            return lambda x: getattr(faker, protocol)()
        if isinstance(field, EmailField): return lambda x: faker.email()
        if isinstance(field, CommaSeparatedIntegerField):
            return lambda x: provider.comma_sep_ints()

        if isinstance(field, BinaryField): return lambda x: provider.binary()
        if isinstance(field, ImageField): return lambda x: provider.file_name()
        if isinstance(field, FilePathField): return lambda x: provider.file_name()
        if isinstance(field, FileField): return lambda x: provider.file_name()

        if isinstance(field, CharField):
            if field.choices:
                return lambda x: random.choice(field.choices)[0]
            return lambda x: faker.text(field.max_length) if field.max_length >= 5 else faker.word()
        if isinstance(field, TextField): return lambda x: faker.text()

        if isinstance(field, DateTimeField):
            # format with timezone if it is active
            return lambda x: _timezone_format(faker.date_time())
        if isinstance(field, DateField): return lambda x: faker.date()
        if isinstance(field, TimeField): return lambda x: faker.time()
        raise AttributeError(field)