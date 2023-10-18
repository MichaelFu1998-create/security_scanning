def create(cls, data, id_=None):
        """Create a deposit.

        Initialize the follow information inside the deposit:

        .. code-block:: python

            deposit['_deposit'] = {
                'id': pid_value,
                'status': 'draft',
                'owners': [user_id],
                'created_by': user_id,
            }

        The deposit index is updated.

        :param data: Input dictionary to fill the deposit.
        :param id_: Default uuid for the deposit.
        :returns: The new created deposit.
        """
        data.setdefault('$schema', current_jsonschemas.path_to_url(
            current_app.config['DEPOSIT_DEFAULT_JSONSCHEMA']
        ))
        if '_deposit' not in data:
            id_ = id_ or uuid.uuid4()
            cls.deposit_minter(id_, data)

        data['_deposit'].setdefault('owners', list())
        if current_user and current_user.is_authenticated:
            creator_id = int(current_user.get_id())

            if creator_id not in data['_deposit']['owners']:
                data['_deposit']['owners'].append(creator_id)

            data['_deposit']['created_by'] = creator_id

        return super(Deposit, cls).create(data, id_=id_)