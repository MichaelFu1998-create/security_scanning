def from_env(cls, reactor=None, env=os.environ):
        """
        Create a Vault client with configuration from the environment. Supports
        a limited number of the available config options:
        https://www.vaultproject.io/docs/commands/index.html#environment-variables
        https://github.com/hashicorp/vault/blob/v0.11.3/api/client.go#L28-L40

        Supported:
        - ``VAULT_ADDR``
        - ``VAULT_CACERT``
        - ``VAULT_CLIENT_CERT``
        - ``VAULT_CLIENT_KEY``
        - ``VAULT_TLS_SERVER_NAME``
        - ``VAULT_TOKEN``

        Not currently supported:
        - ``VAULT_CAPATH``
        - ``VAULT_CLIENT_TIMEOUT``
        - ``VAULT_MAX_RETRIES``
        - ``VAULT_MFA``
        - ``VAULT_RATE_LIMIT``
        - ``VAULT_SKIP_VERIFY``
        - ``VAULT_WRAP_TTL``
        """
        address = env.get('VAULT_ADDR', 'https://127.0.0.1:8200')
        # This seems to be what the Vault CLI defaults to
        token = env.get('VAULT_TOKEN', 'TEST')

        ca_cert = env.get('VAULT_CACERT')
        tls_server_name = env.get('VAULT_TLS_SERVER_NAME')
        client_cert = env.get('VAULT_CLIENT_CERT')
        client_key = env.get('VAULT_CLIENT_KEY')
        cf = ClientPolicyForHTTPS.from_pem_files(
            caKey=ca_cert, privateKey=client_key, certKey=client_cert,
            tls_server_name=tls_server_name
        )
        client, reactor = default_client(reactor, contextFactory=cf)

        return cls(address, token, client=client, reactor=reactor)