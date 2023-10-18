def _get_profile(self, profile_id):
        '''dict: Return the profile with the received ID as a dict (None if it
        doesn't exist).'''
        profile_metadata = self._registry.get(profile_id)
        if not profile_metadata:
            return

        path = self._get_absolute_path(profile_metadata.get('schema_path'))
        url = profile_metadata.get('schema')
        if path:
            try:
                return self._load_json_file(path)
            except IOError as local_exc:
                if not url:
                    raise local_exc

                try:
                    return self._load_json_url(url)
                except IOError:
                    msg = (
                        'Error loading profile locally at "{path}" '
                        'and remotely at "{url}".'
                    ).format(path=path, url=url)
                    six.raise_from(IOError(msg), local_exc)
        elif url:
            return self._load_json_url(url)