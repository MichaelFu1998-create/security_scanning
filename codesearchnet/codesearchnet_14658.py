def put(self,
            name,
            value=None,
            modify=False,
            metadata=None,
            description='',
            encrypt=True,
            lock=False,
            key_type='secret',
            add=False):
        """Put a key inside the stash

        if key exists and modify true: delete and create
        if key exists and modify false: fail
        if key doesn't exist and modify true: fail
        if key doesn't exist and modify false: create

        `name` is unique and cannot be changed.

        `value` must be provided if the key didn't already exist, otherwise,
        the previous value will be retained.

        `created_at` will be left unmodified if the key
        already existed. Otherwise, the current time will be used.

        `modified_at` will be changed to the current time
        if the field is being modified.

        `metadata` will be updated if provided. If it wasn't
        provided the field from the existing key will be used and the
        same goes for the `uid` which will be generated if it didn't
        previously exist.

        `lock` will lock the key to prevent it from being modified or deleted

        `add` allows to add values to an existing key instead of overwriting.

        Returns the id of the key in the database
        """
        def assert_key_is_unlocked(existing_key):
            if existing_key and existing_key.get('lock'):
                raise GhostError(
                    'Key `{0}` is locked and therefore cannot be modified. '
                    'Unlock the key and try again'.format(name))

        def assert_value_provided_for_new_key(value, existing_key):
            if not value and not existing_key.get('value'):
                raise GhostError('You must provide a value for new keys')

        self._assert_valid_stash()
        self._validate_key_schema(value, key_type)
        if value and encrypt and not isinstance(value, dict):
            raise GhostError('Value must be of type dict')

        # TODO: This should be refactored. `_handle_existing_key` deletes
        # the key rather implicitly. It shouldn't do that.
        # `existing_key` will be an empty dict if it doesn't exist
        key = self._handle_existing_key(name, modify or add)
        assert_key_is_unlocked(key)
        assert_value_provided_for_new_key(value, key)

        new_key = dict(name=name, lock=lock)
        if value:
            # TODO: fix edge case in which encrypt is false and yet we might
            # try to add to an existing key. encrypt=false is only used when
            # `load`ing into a new stash, but someone might use it directly
            # from the API.
            if add:
                value = self._update_existing_key(key, value)
            new_key['value'] = self._encrypt(value) if encrypt else value
        else:
            new_key['value'] = key.get('value')

        # TODO: Treat a case in which we try to update an existing key
        # but don't provide a value in which nothing will happen.
        new_key['description'] = description or key.get('description')
        new_key['created_at'] = key.get('created_at') or _get_current_time()
        new_key['modified_at'] = _get_current_time()
        new_key['metadata'] = metadata or key.get('metadata')
        new_key['uid'] = key.get('uid') or str(uuid.uuid4())
        new_key['type'] = key.get('type') or key_type

        key_id = self._storage.put(new_key)

        audit(
            storage=self._storage.db_path,
            action='MODIFY' if (modify or add) else 'PUT',
            message=json.dumps(dict(
                key_name=new_key['name'],
                value='HIDDEN',
                description=new_key['description'],
                uid=new_key['uid'],
                metadata=json.dumps(new_key['metadata']),
                lock=new_key['lock'],
                type=new_key['type'])))

        return key_id