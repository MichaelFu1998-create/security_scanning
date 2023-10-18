def guess_format(self, name):
        """
        Returns a faker method based on the field's name
        :param name:
        """
        name = name.lower()
        faker = self.faker
        if re.findall(r'^is[_A-Z]', name): return lambda x: faker.boolean()
        elif re.findall(r'(_a|A)t$', name): return lambda x: _timezone_format(faker.date_time())

        if name in ('first_name', 'firstname', 'first'): return lambda x: faker.first_name()
        if name in ('last_name', 'lastname', 'last'): return lambda x: faker.last_name()

        if name in ('username', 'login', 'nickname'): return lambda x:faker.user_name()
        if name in ('email', 'email_address'): return lambda x:faker.email()
        if name in ('phone_number', 'phonenumber', 'phone'): return lambda x:faker.phone_number()
        if name == 'address': return lambda x:faker.address()
        if name == 'city': return lambda x: faker.city()
        if name == 'streetaddress': return lambda x: faker.street_address()
        if name in ('postcode', 'zipcode'): return lambda x: faker.postcode()
        if name == 'state': return lambda x: faker.state()
        if name == 'country': return lambda x: faker.country()
        if name == 'title': return lambda x: faker.sentence()
        if name in ('body', 'summary', 'description'): return lambda x: faker.text()