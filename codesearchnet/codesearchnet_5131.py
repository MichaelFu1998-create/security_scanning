def __get_ssh_keys_id_or_fingerprint(ssh_keys, token, name):
        """
            Check and return a list of SSH key IDs or fingerprints according
            to DigitalOcean's API. This method is used to check and create a
            droplet with the correct SSH keys.
        """
        ssh_keys_id = list()
        for ssh_key in ssh_keys:
            if type(ssh_key) in [int, type(2 ** 64)]:
                ssh_keys_id.append(int(ssh_key))

            elif type(ssh_key) == SSHKey:
                ssh_keys_id.append(ssh_key.id)

            elif type(ssh_key) in [type(u''), type('')]:
                # ssh_key could either be a fingerprint or a public key
                #
                # type(u'') and type('') is the same in python 3 but
                # different in 2. See:
                # https://github.com/koalalorenzo/python-digitalocean/issues/80
                regexp_of_fingerprint = '([0-9a-fA-F]{2}:){15}[0-9a-fA-F]'
                match = re.match(regexp_of_fingerprint, ssh_key)

                if match is not None and match.end() == len(ssh_key) - 1:
                    ssh_keys_id.append(ssh_key)

                else:
                    key = SSHKey()
                    key.token = token
                    results = key.load_by_pub_key(ssh_key)

                    if results is None:
                        key.public_key = ssh_key
                        key.name = "SSH Key %s" % name
                        key.create()
                    else:
                        key = results

                    ssh_keys_id.append(key.id)
            else:
                raise BadSSHKeyFormat(
                    "Droplet.ssh_keys should be a list of IDs, public keys"
                    + " or fingerprints."
                )

        return ssh_keys_id